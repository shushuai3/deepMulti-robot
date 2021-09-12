// Convert 8bit image to RGB888 images, output image has wrong pixels
// Run in terminal: gcc -o hello hello.c;  Then run ./hello.c
// https://stackoverflow.com/questions/2693631/read-ppm-file-and-store-it-in-an-array-coded-with-c

#include <stdio.h>
#include <stdlib.h>
#include "img_proc.h"

#define RGB_COMPONENT_COLOR 255

typedef struct {
     int x, y;
     char *data;
} PPMImage;

typedef struct {
     int x, y;
     char *data;
} PPMImage_grey;

static PPMImage_grey *readPPM(const char *filename)
{
    char buff[16];
    PPMImage_grey *img;
    FILE *fp;
    int c, rgb_comp_color;
    //open PPM file for reading
    fp = fopen(filename, "rb");
    if (!fp) {
        fprintf(stderr, "Unable to open file '%s'\n", filename);
        exit(1);
    }
    //read image format
    if (!fgets(buff, sizeof(buff), fp)) {
        perror(filename);
        exit(1);
    }
    //check the image format
    if (buff[0] != 'P' || buff[1] != '5') {
        fprintf(stderr, "Invalid image format (must be 'P5')\n");
        exit(1);
    }
    //alloc memory form image
    img = (PPMImage_grey *)malloc(sizeof(PPMImage_grey));
    if (!img) {
         fprintf(stderr, "Unable to allocate memory\n");
         exit(1);
    }
    //check for comments
    c = getc(fp);
    while (c == '#') {
    while (getc(fp) != '\n') ;
         c = getc(fp);
    }
    ungetc(c, fp);
    //read image size information
    if (fscanf(fp, "%d %d", &img->x, &img->y) != 2) {
         fprintf(stderr, "Invalid image size (error loading '%s')\n", filename);
         exit(1);
    }

    //read rgb component
    if (fscanf(fp, "%d", &rgb_comp_color) != 1) {
         fprintf(stderr, "Invalid rgb component (error loading '%s')\n", filename);
         exit(1);
    }

    //check rgb component depth
    if (rgb_comp_color!= RGB_COMPONENT_COLOR) {
         fprintf(stderr, "'%s' does not have 8-bits components\n", filename);
         exit(1);
    }

    while (fgetc(fp) != '\n') ;
    //memory allocation for pixel data
    img->data = (char*)malloc(img->x * img->y * sizeof(char));

    if (!img) {
         fprintf(stderr, "Unable to allocate memory\n");
         exit(1);
    }

    //read pixel data from file
    if (fread(img->data, img->x, img->y, fp) != img->y) {
         fprintf(stderr, "Error loading image '%s'\n", filename);
         exit(1);
    }

    fclose(fp);
    return img;
}

static PPMImage *ColorPPM(PPMImage_grey *img_grey)
{
    PPMImage *img;
    img = (PPMImage *)malloc(sizeof(PPMImage));
    img->data = (char*)malloc(3*img->x * img->y * sizeof(char));
    img->x = 320;
    img->y = 224;
    if (!img) {
         fprintf(stderr, "Unable to allocate memory\n");
         exit(1);
    }
    demosaicking(img_grey->data, img->data, 320, 224, 0);
    return img;
}


void writePPM(const char *filename, PPMImage *img)
{
    FILE *fp;
    //open file for output
    fp = fopen(filename, "wb");
    if (!fp) {
         fprintf(stderr, "Unable to open file '%s'\n", filename);
         exit(1);
    }

    //write the header file
    //image format
    fprintf(fp, "P6\n");

    //image size
    fprintf(fp, "%d %d\n",img->x,img->y);

    // rgb component depth
    fprintf(fp, "%d\n",RGB_COMPONENT_COLOR);

    // pixel data
    fwrite(img->data, 3 * img->x, img->y, fp);
    fclose(fp);
}

void main(){
    printf("Hello World\n");
    PPMImage_grey *image_grey;
    PPMImage *image_color;
    image_grey  = readPPM("test.ppm");
    image_color = ColorPPM(image_grey);
    writePPM("test_color.ppm",image_color);
    printf("Press any key...");
    getchar();
}