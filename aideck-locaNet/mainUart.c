/*
 * Copyright 2019 GreenWaves Technologies, SAS
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *     http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */

#include "pmsis.h"
#include "bsp/flash/hyperflash.h"
#include "bsp/bsp.h"
#include "bsp/buffer.h"
#include "bsp/camera/himax.h"
#include "bsp/ram.h"
#include "bsp/ram/hyperram.h"
#include "img_proc.h"
#include "main.h"

/* Defines */
// #define NUM_CLASSES 	1001
#define AT_OUTPUT_SIZE  2240
#define AT_INPUT_SIZE 	(AT_INPUT_WIDTH*AT_INPUT_HEIGHT*AT_INPUT_COLORS)

#define __XSTR(__s) __STR(__s)
#define __STR(__s) #__s 
#ifdef HAVE_CAMERA	
	#define CAMERA_WIDTH    (324)
	#define CAMERA_HEIGHT   (244)
	#define CAMERA_SIZE   	(CAMERA_HEIGHT*CAMERA_WIDTH)
#endif

typedef signed char NETWORK_OUT_TYPE;

// Global Variables
struct pi_device camera;
static pi_buffer_t buffer;
struct pi_device HyperRam;
struct pi_device uart;
L2_MEM char *uartData;

L2_MEM NETWORK_OUT_TYPE *ResOut;
static uint32_t l3_buff;
AT_HYPERFLASH_FS_EXT_ADDR_TYPE AT_L3_ADDR = 0;

static void RunNetwork()
{
  printf("Running on cluster\n");
#ifdef PERF
  printf("Start timer\n");
  gap_cl_starttimer();
  gap_cl_resethwtimer();
#endif
  AT_CNN((unsigned char *) l3_buff, ResOut);
  printf("Runner completed\n");

}

int body(void)
{
	// Voltage-Frequency settings
	uint32_t voltage =1200;
	pi_freq_set(PI_FREQ_DOMAIN_FC, FREQ_FC*1000*1000);
	pi_freq_set(PI_FREQ_DOMAIN_CL, FREQ_CL*1000*1000);
	//PMU_set_voltage(voltage, 0);
	printf("Set VDD voltage as %.2f, FC Frequency as %d MHz, CL Frequency = %d MHz\n", 
		(float)voltage/1000, FREQ_FC, FREQ_CL);

	// Initialize the ram 
  	struct pi_hyperram_conf hyper_conf;
  	pi_hyperram_conf_init(&hyper_conf);
  	pi_open_from_conf(&HyperRam, &hyper_conf);
	if (pi_ram_open(&HyperRam))
	{
		printf("Error ram open !\n");
		pmsis_exit(-3);
	}

	// Allocate L3 buffer to store input data 
	if (pi_ram_alloc(&HyperRam, &l3_buff, (uint32_t) AT_INPUT_SIZE))
	{
		printf("Ram malloc failed !\n");
		pmsis_exit(-4);
	}

#ifdef HAVE_CAMERA
	// Allocate temp buffer for camera data
	uint8_t* Input_1 = (uint8_t*) pmsis_l2_malloc(CAMERA_SIZE*sizeof(char));
	if(!Input_1){
		printf("Failed allocation!\n");
		pmsis_exit(1);
	}

    uint8_t* Input_3 = (uint8_t*) pmsis_l2_malloc(AT_INPUT_SIZE*sizeof(char));
	if(!Input_3){
		printf("Failed allocation!\n");
		pmsis_exit(1);
	}

    printf("debug point\n");
   
    // ------ open camera
    struct pi_himax_conf cam_conf;
    pi_himax_conf_init(&cam_conf);
    cam_conf.format = PI_CAMERA_QVGA;
    pi_open_from_conf(&camera, &cam_conf);
    if (pi_camera_open(&camera))
    {
        printf("Failed to open camera\n");
        pmsis_exit(-1);
    }
    // pi_camera_control(&camera, PI_CAMERA_CMD_AEG_INIT, 0);
    printf("Open Himax camera\n");
    
    // ------ camera rotation and qvga mode
    pi_camera_control(&camera, PI_CAMERA_CMD_START, 0);
    uint8_t set_value=3;
    uint8_t reg_value;
    pi_camera_reg_set(&camera, IMG_ORIENTATION, &set_value);
    pi_time_wait_us(1000000);
    pi_camera_reg_get(&camera, IMG_ORIENTATION, &reg_value);
    if (set_value!=reg_value)
    {
        printf("Failed to rotate camera image\n");
        return -1;
    }
    pi_camera_control(&camera, PI_CAMERA_CMD_STOP, 0);
    pi_camera_control(&camera, PI_CAMERA_CMD_AEG_INIT, 0);

    set_value=1;
    pi_camera_reg_set(&camera, QVGA_WIN_EN, &set_value);
    pi_camera_reg_get(&camera, QVGA_WIN_EN, &reg_value);
    printf("qvga window enabled %d\n",reg_value);

#else
	// Allocate temp buffer for image data
	int8_t* Input_1 = (int8_t*) pmsis_l2_malloc(AT_INPUT_SIZE*sizeof(char));
	if(!Input_1){
		printf("Failed allocation!\n");
		pmsis_exit(1);
	}

	char *ImageName = __XSTR(AT_IMAGE);
	printf("Reading image from %s\n",ImageName);

	//Reading Image from Bridge
	img_io_out_t type = IMGIO_OUTPUT_CHAR;
	if (ReadImageFromFile(ImageName, AT_INPUT_WIDTH, AT_INPUT_HEIGHT, AT_INPUT_COLORS, Input_1, AT_INPUT_SIZE*sizeof(char), type, 0)) {
		printf("Failed to load image %s\n", ImageName);
		pmsis_exit(-1);
	}
	printf("Finished reading image %s\n", ImageName);
#endif

	//move input image to L3 Hyperram
#ifdef HAVE_CAMERA

#else
	// write greyscale image to RAM
	pi_ram_write(&HyperRam, (l3_buff), Input_1, (uint32_t) AT_INPUT_SIZE);
	pmsis_l2_malloc_free(Input_1, AT_INPUT_SIZE*sizeof(char));
#endif

	// Open the cluster
	struct pi_device cluster_dev;
	struct pi_cluster_conf conf;
	pi_cluster_conf_init(&conf);
	pi_open_from_conf(&cluster_dev, (void *)&conf);
	pi_cluster_open(&cluster_dev);

	// Task setup
	struct pi_cluster_task *task = pmsis_l2_malloc(sizeof(struct pi_cluster_task));
	if(task==NULL) {
	  printf("pi_cluster_task alloc Error!\n");
	  pmsis_exit(-1);
	}
	printf("Stack size is %d and %d\n",STACK_SIZE,SLAVE_STACK_SIZE );
	memset(task, 0, sizeof(struct pi_cluster_task));
	task->entry = &RunNetwork;
	task->stack_size = STACK_SIZE;
	task->slave_stack_size = SLAVE_STACK_SIZE;
	task->arg = NULL;

	// Allocate the output tensor
	ResOut = (NETWORK_OUT_TYPE *) AT_L2_ALLOC(0, AT_OUTPUT_SIZE*sizeof(NETWORK_OUT_TYPE));
	if (ResOut==0) {
		printf("Failed to allocate Memory for Result (%ld bytes)\n", 2*sizeof(char));
		return 1;
	}

    uartData = (char *) pmsis_l2_malloc(5*sizeof(char));
	if (uartData==0) {
		printf("Failed to allocate Memory for uartData (%ld bytes)\n", 2*sizeof(char));
		return 1;
	}
    uartData[0] = 0xfe;
    uartData[1] = 0xfe;
    struct pi_uart_conf uart_conf;
    /* Init & open uart. */
    pi_uart_conf_init(&uart_conf);
    // uart_conf.enable_tx = 1;
    // uart_conf.enable_rx = 0;
    uart_conf.baudrate_bps = 115200;
    pi_open_from_conf(&uart, &uart_conf);
    if (pi_uart_open(&uart))
    {
        printf("Uart open failed !\n");
        pmsis_exit(-1);
    }
    pi_uart_open(&uart);

    static struct pi_device gpio_device;
    pi_gpio_pin_configure(&gpio_device, 2, PI_GPIO_OUTPUT);
    static int led_val = 0;
    pi_gpio_pin_write(&gpio_device, 2, led_val);
	// Network Constructor
	// IMPORTANT: MUST BE CALLED AFTER THE CLUSTER IS ON!
	int err_const = AT_CONSTRUCT();
	if (err_const)
	{
	  printf("Graph constructor exited with error: %d\n", err_const);
	  return 1;
	}
	printf("Network Constructor was OK!\n");

    while(1){
	// Get an image 
    pi_camera_control(&camera, PI_CAMERA_CMD_START, 0);
    pi_camera_capture(&camera, Input_1, CAMERA_SIZE);
    pi_camera_control(&camera, PI_CAMERA_CMD_STOP, 0);
    // Image Cropping to [ AT_INPUT_HEIGHT x AT_INPUT_WIDTH ]
    int ps=0;
    for(int i =0;i<CAMERA_HEIGHT;i++){
    	for(int j=0;j<CAMERA_WIDTH;j++){
    		if (i<234 && i>9 && j<322 && j>1){
    			Input_1[ps] = Input_1[i*CAMERA_WIDTH+j];
    			ps++;        			
    		}
    	}
    }
    // Copy Single Channel Greyscale to 3 channel RGB: CH0-CH1-CH2 
	// pi_ram_write(&HyperRam, (l3_buff), 									Input_1, (uint32_t) AT_INPUT_WIDTH*AT_INPUT_HEIGHT);
	// pi_ram_write(&HyperRam, (l3_buff+AT_INPUT_WIDTH*AT_INPUT_HEIGHT), 	Input_1, (uint32_t) AT_INPUT_WIDTH*AT_INPUT_HEIGHT);
	// pi_ram_write(&HyperRam, (l3_buff+2*AT_INPUT_WIDTH*AT_INPUT_HEIGHT), Input_1, (uint32_t) AT_INPUT_WIDTH*AT_INPUT_HEIGHT);
	// pmsis_l2_malloc_free(Input_1, CAMERA_SIZE*sizeof(char));
    demosaicking(Input_1, Input_3, 320, 224, 0);
    // WriteImageToFile("../../../img.ppm", 320, 224, sizeof(uint32_t), Input_3, RGB888_IO);
    pi_ram_write(&HyperRam, (l3_buff), Input_3, (uint32_t) AT_INPUT_SIZE);

	// Dispatch task on the cluster 
	pi_cluster_send_task_to_cl(&cluster_dev, task);

	//Check Results
	int outclass, MaxPrediction = 0;

    static signed char max = -100;
    static char max_index_x = -100;
    static char max_index_y = -100;
    // for(int i=0; i<28; i++){
    //     for(int j=0; j<40; j++){
    //         printf("%d ",ResOut[(i*40+j)]);
    //         if(max < ResOut[(i*40+j)]){
    //             max = ResOut[(i*40+j)];
    //             max_index_x = i;
    //             max_index_y = j;
    //         }
    //     }
    //     printf("\n");
    // }
    // printf("The largest value: %3d Index H: %3d W: %3d\n",max, max_index_x, max_index_y);

    max = -100;
    for(int i=0; i<28; i++){
        for(int j=0; j<40; j++){
            // printf("%d ",ResOut[1120+(i*40+j)]);
            if(max < ResOut[1120+(i*40+j)]){
                max = ResOut[1120+(i*40+j)];
                max_index_x = i;
                max_index_y = j;
            }
        }
        // printf("\n");
    }
    printf("The largest value: %3d Index H: %3d W: %3d\n",max, max_index_x, max_index_y);

    if(max > -20){
        uartData[2] = max_index_x;
        uartData[3] = max_index_y;
        // uartData[4] = ResOut[(max_index_x*40+max_index_y)]+128;
        uartData[4] = max+64;
        pi_uart_write(&uart, uartData, 5);
        // pi_uart_write(&uart, &value, 1);
    }
    led_val = 1 - led_val;
    pi_gpio_pin_write(&gpio_device, 2, led_val);
    // printf("Model:\t%s\n\n", __XSTR(AT_MODEL_PREFIX));
	// printf("Predicted class:\t%d\n", outclass);
	// printf("With confidence:\t%d\n", MaxPrediction);
    }


	// Performance counters
#ifdef PERF
	{
		unsigned int TotalCycles = 0, TotalOper = 0;
		printf("\n");
		for (int i=0; i<(sizeof(AT_GraphPerf)/sizeof(unsigned int)); i++) {
			printf("%45s: Cycles: %10d, Operations: %10d, Operations/Cycle: %f\n", AT_GraphNodeNames[i], AT_GraphPerf[i], AT_GraphOperInfosNames[i], ((float) AT_GraphOperInfosNames[i])/ AT_GraphPerf[i]);
			TotalCycles += AT_GraphPerf[i]; TotalOper += AT_GraphOperInfosNames[i];
		}
		printf("\n");
		printf("%45s: Cycles: %10d, Operations: %10d, Operations/Cycle: %f\n", "Total", TotalCycles, TotalOper, ((float) TotalOper)/ TotalCycles);
		printf("\n");
	}
#endif

	// Netwrok Destructor
	AT_DESTRUCT();
	pi_cluster_close(&cluster_dev);
	pmsis_exit(0);

	return 0;
}


int main(void)
{
    printf("\n\n\t *** ImageNet classification on GAP ***\n");
    return pmsis_kickoff((void *) body);
}

