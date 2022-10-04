SHELL:=/bin/bash
DATE:=$(shell date +'%d.%m.%y-%Hh-%Mm-%Ss')
LIB3:=a.pvl.pvl
TMP:=tmp.pvl.pvl
ifdef ike
  PVM4 = ikeV2_HF_EC.pv
  PV = ikeV2_HF_EC.pv.pv
  M4:= -D M_IKE ${m4}
  FILE:=IKE
  LIB3:=MDH.pvl.pvl
endif
ifdef ike_s
  PVM4 = simplified_ikeV2_HF_EC.pv
  PV = simplified_ikeV2_HF_EC.pv.pv
  M4:= -D M_IKE_S ${m4}
  FILE:=IKE_S
  LIB3:=MDH.pvl.pvl
endif
ifdef sigma
  PVM4 = sigma_HF_EC.pv
  PV = sigma_HF_EC.pv.pv
  M4:= -D M_SIGMA ${m4}
  FILE:=SIGMA
endif
comma:= +
empty:=
space:= $(empty) $(empty)
D:=-D
m4_STRIPPED:= $(subst $(space),$(comma),$(filter-out $(D),$(m4)))
NAME="${log}__file:$(FILE)_m4:${m4_STRIPPED}_date:${DATE}"
LOG_FOLDER:="LOGs/${NAME}"
LOG_FILE:="LOGs/${NAME}/LOG.txt"
HTML_FILE:="LOGs/${NAME}/index.html"
LIBM4 = chosenPrefixM4_HF_EC.pvl
LIB = chosenPrefixM4_HF_EC.pvl.pvl
LIB2M4 = MDH.pvl
LIB2 = MDH.pvl.pvl
LIBS = -lib $(LIB) -lib $(LIB2)
ifdef html
	FLAGS_PV = -html $(LOG_FOLDER)
endif
ifdef m4
	FLAGS_M4 = $(M4)	# TODO: Use better syntax and parse it here
endif
ifndef debug
	OUTPUT:=  | grep -E "error|Error|RESULT|avgtext"
endif

all:
	@mkdir -p $(LOG_FOLDER)
	@echo " ---> Options chosen:" | tee -a $(LOG_FILE)
	@m4 $(FLAGS_M4) pretty.m4 | tee -a $(LOG_FILE)
	@m4 $(FLAGS_M4) $(LIB2M4) > $(LIB2)
	@sed -e 's/H(/H_(/g' $(LIB2) > $(TMP)
	@cat $(TMP) >> $(LIB3)
	@cat $(LIB2) | tee -a $(LOG_FILE)
	@m4 $(FLAGS_M4) $(PVM4) > $(PV)
	@m4 $(FLAGS_M4) $(LIBM4) > $(LIB)
	@echo "\n ---> Running ProVerif, log file and html outputs in $(LOG_FILE). Only displaying errors and analysis results ..." | tee -a $(LOG_FILE)
	@date +'START DATE: %d.%m.%y -- %T' | tee -a $(LOG_FILE)
	@m4 $(FLAGS_M4) pretty.m4 >> $(LOG_FILE)
	time proverif $(FLAGS_PV) $(LIBS) $(PV) 2>&1 | tee -a $(LOG_FILE) $(OUTPUT)
	@date +'END DATE: %d.%m.%y -- %T' | tee -a $(LOG_FILE)
	@echo " ===> Done, full LOG in $(LOG_FILE)."
# @m4 $(FLAGS_M4) pretty.m4
	@echo " ---> Openingn $(HTML_FILE)."
# @firefox $(HTML_FILE)

debug:
	@mkdir -p $(LOG_FOLDER)
	@echo " ---> Options chosen:" | tee -a $(LOG_FILE)
	m4 $(FLAGS_M4) pretty.m4 | tee -a $(LOG_FILE)
	m4 $(FLAGS_M4) $(LIB2M4) | tee -a $(LOG_FILE)
	m4 $(FLAGS_M4) $(LIBM4) > $(LIB)
	m4 $(FLAGS_M4) $(LIB2M4) > $(LIB2)
	sed -e 's/H(/H_(/g' $(LIB2) > $(TMP)
	cat $(TMP) >> $(LIB3)
	cat $(LIB2) | tee -a $(LOG_FILE)
	m4 $(FLAGS_M4) $(PVM4) > $(PV)
	m4 $(FLAGS_M4) $(LIBM4) > $(LIB)
	echo "\n ---> Running ProVerif, log file and html outputs in $(LOG_FILE). Only displaying errors and analysis results ..." | tee -a $(LOG_FILE)
	date +'START DATE: %d.%m.%y -- %T' | tee -a $(LOG_FILE)
	@m4 $(FLAGS_M4) pretty.m4 >> $(LOG_FILE)
	time proverif $(FLAGS_PV) $(LIBS) $(PV) #2>&1 | tee -a $(LOG_FILE) $(OUTPUT)
	@date +'END DATE: %d.%m.%y -- %T' | tee -a $(LOG_FILE)
	@echo " ===> Done, full LOG in $(LOG_FILE)."
# @m4 $(FLAGS_M4) pretty.m4
	@echo " ---> Openingn $(HTML_FILE)."
# @firefox $(HTML_FILE)

clean:
	rm *.pvl.pvl *.pv.pv
