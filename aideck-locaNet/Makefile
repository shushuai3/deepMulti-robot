# Copyright (C) 2017 GreenWaves Technologies
# All rights reserved.

# This software may be modified and distributed under the terms
# of the BSD license.  See the LICENSE file for details.

# LocaNet for monocular relative localization of multiple Crazyflies
# Author: Shushuai Li, TUDelft
# Paper: https://arxiv.org/abs/2105.12797

ifndef GAP_SDK_HOME
  $(error Source sourceme in gap_sdk first)
endif

MODEL_PREFIX=loca
AT_INPUT_WIDTH=320
AT_INPUT_HEIGHT=224
AT_INPUT_COLORS=3
NNTOOL_SCRIPT=models/nntool_script

## AT GENERATED NAMES
AT_CONSTRUCT = $(MODEL_PREFIX)CNN_Construct
AT_DESTRUCT = $(MODEL_PREFIX)CNN_Destruct
AT_CNN = $(MODEL_PREFIX)CNN
AT_L3_ADDR = $(MODEL_PREFIX)_L3_Flash

# QUANT_FLAG ?= -q # if quantized already

IMAGE=$(CURDIR)/images/0026.ppm

MODEL_L3_EXEC=hram
MODEL_L3_CONST=hflash

QUANT_BITS=8
BUILD_DIR=BUILD
$(info Building GAP8 mode with $(QUANT_BITS) bit quantization)
MODEL_SQ8=1 # use scale based quantization (tflite-like)
NNTOOL_SCRIPT?=models/nntool_scripts/nntool_script
MODEL_SUFFIX=_SQ8BIT
TRAINED_TFLITE_MODEL=models/$(MODEL_PREFIX).tflite

include common/model_decl.mk

# Here we set the default memory allocation for the generated kernels
# REMEMBER THAT THE L1 MEMORY ALLOCATION MUST INCLUDE SPACE
# FOR ALLOCATED STACKS!
CLUSTER_STACK_SIZE?=6096
CLUSTER_SLAVE_STACK_SIZE?=1024
TOTAL_STACK_SIZE = $(shell expr $(CLUSTER_STACK_SIZE) \+ $(CLUSTER_SLAVE_STACK_SIZE) \* 7)
ifeq '$(TARGET_CHIP_FAMILY)' 'GAP9'
	FREQ_CL?=50
	FREQ_FC?=50
	MODEL_L1_MEMORY=$(shell expr 125000 \- $(TOTAL_STACK_SIZE))
	MODEL_L2_MEMORY=1300000
	MODEL_L3_MEMORY=8388608
else
	ifeq '$(TARGET_CHIP)' 'GAP8_V3'
		FREQ_CL?=175
	else
		FREQ_CL?=50
	endif
	FREQ_FC?=250
	MODEL_L1_MEMORY=$(shell expr 60000 \- $(TOTAL_STACK_SIZE))
	MODEL_L2_MEMORY?=200000
	MODEL_L3_MEMORY=8000000
endif


pulpChip = GAP
PULP_APP = imagenet
USE_PMSIS_BSP=1

APP = imagenet
MAIN ?= main.c
APP_SRCS += $(MAIN) $(MODEL_GEN_C) $(MODEL_COMMON_SRCS) $(CNN_LIB) $(TILER_BILINEAR_RESIZE_KERNEL_PATH)/ResizeBasicKernels.c

APP_CFLAGS += -g -O3 -mno-memcpy -fno-tree-loop-distribute-patterns
# list of includes file
APP_CFLAGS += -I. -I$(MODEL_COMMON_INC) -I$(TILER_EMU_INC) -I$(TILER_INC) $(CNN_LIB_INCLUDE) -I$(MODEL_BUILD) -I$(MODEL_HEADERS)
# pass also macro defines to the compiler
APP_CFLAGS += -DAT_MODEL_PREFIX=$(MODEL_PREFIX) $(MODEL_SIZE_CFLAGS)
APP_CFLAGS += -DSTACK_SIZE=$(CLUSTER_STACK_SIZE) -DSLAVE_STACK_SIZE=$(CLUSTER_SLAVE_STACK_SIZE)
APP_CFLAGS += -DAT_IMAGE=$(IMAGE) -DPERF -DFREQ_FC=$(FREQ_FC) -DFREQ_CL=$(FREQ_CL)
APP_CFLAGS += -DAT_CONSTRUCT=$(AT_CONSTRUCT) -DAT_DESTRUCT=$(AT_DESTRUCT) -DAT_CNN=$(AT_CNN) -DAT_L3_ADDR=$(AT_L3_ADDR)

HAVE_CAMERA?=0
HAVE_LCD?=0
ifeq ($(HAVE_CAMERA), 1)
	APP_CFLAGS += -DHAVE_CAMERA
endif
ifeq ($(HAVE_LCD), 1)
	APP_CFLAGS += -DHAVE_LCD
endif

# this line is needed to flash into the chip the model tensors 
# and other constants needed by the Autotiler
READFS_FILES=$(abspath $(MODEL_TENSORS))
PLPBRIDGE_FLAGS += -f

# all depends on the model
all:: model

clean:: clean_model

clean_at_model::
	$(RM) $(MODEL_GEN_C)

# convert h5 to tflite
MODEL_CONVERT = models/h5_to_tflite.py
MODEL_H5 = models/$(MODEL_PREFIX).h5
$(TRAINED_TFLITE_MODEL): $(MODEL_H5)
	$(MODEL_PYTHON) $(MODEL_CONVERT) $< $@

include common/model_rules.mk
$(info APP_SRCS... $(APP_SRCS))
$(info APP_CFLAGS... $(APP_CFLAGS))
include $(RULES_DIR)/pmsis_rules.mk