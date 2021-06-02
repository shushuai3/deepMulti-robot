APP = test
APP_SRCS += test.c $(GAP_LIB_PATH)/img_io/ImgIO.c
APP_INC  += . $(GAP_LIB_PATH)/include

APP_CFLAGS += -O3 -g

ifeq ($(write), 1)
APP_CFLAGS      += -DWRITE_DATASET=1
endif

ifeq ($(write), 0)
APP_CFLAGS      += -DWRITE_DATASET=0
endif

PMSIS_OS ?= pulp_os

clean::
	rm -rf img_raw.ppm img_color.ppm img_gray.ppm

include $(RULES_DIR)/pmsis_rules.mk
