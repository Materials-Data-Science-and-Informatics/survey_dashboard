#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct 26 09:27:45 2021

@author: s.gerlich
"""

##########################################
############### DICTIONARY ###############
########## RENAME COLUMN NAMES ###########
########################################## 

# Dictionary to rename columns in df for better readability 

HCS_colnamesDict = {
        "PERBG1":"centerAffiliation",
        "PERBG1_other":"centerAffiliation_other",
        "PERBG2":"researchFieldHGF",
        "PERBG3": "researchArea",
        "PERBG3_other":"researchArea_other",
        "PERBG3ING":"researchAreaING",
        "PERBG3ING_other":"researchAreaING_other",
        "PERBG3GEO":"researchAreaGEO",
        "PERBG3GEO_other":"researchAreaGEO_other",
        "PERBG3MATH":"researchAreaMATH",
        "PERBG3MATH_other":"researchAreaMATH_other",
        "PERBG3PHYS":"researchAreaPHYS",
        "PERBG3PHYS_other":"researchAreaPHYS_other",
        "PERBG3LIFE":"researchAreaLIFE",
        "PERBG3LIFE_other":"researchAreaLIFE_other",
        "PERBG3BIO":"researchAreaBIO",
        "PERBG3BIO_other":"researchAreaBIO_other",
        "PERBG3MED":"researchAreaMED",
        "PERBG3MED_other":"researchAreaMED_other",
        "PERBG3AGRI":"researchAreaAGRI",
        "PERBG3AGRI_other":"researchAreaAGRI_other",
        "PERBG3PSYCH":"researchAreaPSYCH",
        "PERBG3PSYCH_other":"researchAreaPSYCH_other",
        "PERBG3CHEM":"researchAreaCHEM",
        "PERBG3CHEM_other":"researchAreaCHEM_other",
        "PERBG4":"yearsInResearch",
        "PERBG6":"careerLevel",
        "PERBG6_other":"careerLevel_other",
        "PERBG7":"orcid",
        "PERBG8":"fairFamiliarity",
        "RSDP1_1A2":"dataOrigin_MeasVsSim",
        "RSDP1_3A4":"dataOrigin_SelvVsReuse",
        "RSDP1b_1":"dataAmount_lsf",
        "RSDP1c_1":"lsfIdent_1",
        "RSDP1c_2":"lsfIdent_2",
        "RSDP1c_3":"lsfIdent_3",
        "RSDP1c_4":"lsfIdent_4",
        "RSDP1c_5":"lsfIdent_5",
        "RSDP1c_6":"lsfIdent_6",
        "RSDP1c_7":"lsfIdent_7",
        "RSDP1c_8":"lsfIdent_8",
        "RSDP1c_9":"lsfIdent_9",
        "RSDP1c_10":"lsfIdent_10",
        "RSDP1c_11":"lsfIdent_11",
        "RSDP1c_other":"lsfIdent_other",
        "RSDP2_1":"dataGenMethod_1",
        "RSDP2_2":"dataGenMethod_2",
        "RSDP2_3":"dataGenMethod_3",
        "RSDP2_4":"dataGenMethod_4",
        "RSDP2_5":"dataGenMethod_5",
        "RSDP2_6":"dataGenMethod_6",
        "RSDP2_other":"dataGenMethod_other",
        "RSDP2b_1_1":"dataGenMethodSpec_1_1",
        "RSDP2b_1_2":"dataGenMethodSpec_1_2",
        "RSDP2b_1_3":"dataGenMethodSpec_1_3",
        "RSDP2b_2_1":"dataGenMethodSpec_2_1",
        "RSDP2b_2_2":"dataGenMethodSpec_2_2",
        "RSDP2b_2_3":"dataGenMethodSpec_2_3",
        "RSDP2b_3_1":"dataGenMethodSpec_3_1",
        "RSDP2b_3_2":"dataGenMethodSpec_3_2",
        "RSDP2b_3_3":"dataGenMethodSpec_3_3",
        "RSDP2b_4_1":"dataGenMethodSpec_4_1",
        "RSDP2b_4_2":"dataGenMethodSpec_4_2",
        "RSDP2b_4_3":"dataGenMethodSpec_4_3",
        "RSDP2b_5_1":"dataGenMethodSpec_5_1",
        "RSDP2b_5_2":"dataGenMethodSpec_5_2",
        "RSDP2b_5_3":"dataGenMethodSpec_5_3",
        "RSDP2b_6_1":"dataGenMethodSpec_6_1",
        "RSDP2b_6_2":"dataGenMethodSpec_6_2",
        "RSDP2b_6_3":"dataGenMethodSpec_6_3",
        "RSDP2b_7_1":"dataGenMethodSpec_7_1",
        "RSDP2b_7_2":"dataGenMethodSpec_7_2",
        "RSDP2b_7_3":"dataGenMethodSpec_7_3",
        "RSDP3_1":"dataFormats_1",
        "RSDP3_2":"dataFormats_2",
        "RSDP3_3":"dataFormats_3",
        "RSDP3_4":"dataFormats_4",
        "RSDP3_5":"dataFormats_5",
        "RSDP3_6":"dataFormats_6",
        "RSDP3_7":"dataFormats_7",
        "RSDP3_8":"dataFormats_8",
        "RSDP3_9":"dataFormats_9",
        "RSDP3_10":"dataFormats_10",
        "RSDP3_11":"dataFormats_11",
        "RSDP3_12":"dataFormats_12",
        "RSDP3_13":"dataFormats_13",
        "RSDP3_14":"dataFormats_14",
        "RSDP3_15":"dataFormats_15",
        "RSDP3_other":"dataFormats_other",
        "RSDP7":"dataInPublication",
        "RSDP4":"dataGatherTime",
        "RSDP8":"experimentDuration_sub",
        "RSDP11":"dataAnalDuration_sub",
        "RSDP10":"longtermStorage",
        "DTPUB6_1":"pubAmount",
        "DTPUB1b_1":"pubMethod_1",
        "DTPUB1b_2":"pubMethod_2",
        "DTPUB1b_3":"pubMethod_3",
        "DTPUB1b_other":"pubMethod_other",
        "DTPUB5_1":"pubRepo_1",
        "DTPUB5_2":"pubRepo_2",
        "DTPUB5_3":"pubRepo_3",
        "DTPUB5_4":"pubRepo_4",
        "DTPUB5_5":"pubRepo_5",
        "DTPUB3_1":"pubMotivation_1",
        "DTPUB3_2":"pubMotivation_2",
        "DTPUB3_3":"pubMotivation_3",
        "DTPUB3_4":"pubMotivation_4",
        "DTPUB3_5":"pubMotivation_5",
        "DTPUB3_6":"pubMotivation_6",
        "DTPUB3_7":"pubMotivation_7",
        "DTPUB3_other":"pubMotivation_other",
        "DTPUB4a_0":"pubObstaclesA_0",
        "DTPUB4a_1":"pubObstaclesA_1",
        "DTPUB4a_2":"pubObstaclesA_2",
        "DTPUB4a_3":"pubObstaclesA_3",
        "DTPUB4a_4":"pubObstaclesA_4",
        "DTPUB4a_5":"pubObstaclesA_5",
        "DTPUB4a_6":"pubObstaclesA_6",
        "DTPUB4a_7":"pubObstaclesA_7",
        "DTPUB4a_other":"pubObstaclesA_other",
        "DTPUB4b_0":"pubObstaclesB_0",
        "DTPUB4b_1":"pubObstaclesB_1",
        "DTPUB4b_2":"pubObstaclesB_2",
        "DTPUB4b_3":"pubObstaclesB_3",
        "DTPUB4b_4":"pubObstaclesB_4",
        "DTPUB4b_5":"pubObstaclesB_5",
        "DTPUB4b_6":"pubObstaclesB_6",
        "DTPUB4b_7":"pubObstaclesB_7",
        "DTPUB4b_other":"pubObstaclesB_other",
        "RDMPR1_0":"dataStorage_0",
        "RDMPR1_1":"dataStorage_1",
        "RDMPR1_2":"dataStorage_2",
        "RDMPR1_3":"dataStorage_3",
        "RDMPR1_other":"dataStorage_other",
        "RDMPR3_0":"docMethod_0",
        "RDMPR3_1":"docMethod_1",
        "RDMPR3_2":"docMethod_2",
        "RDMPR3_3":"docMethod_3",
        "RDMPR3_other":"docMethod_other",
        "RDMPR7_2":"docMetadata_2",
        "RDMPR7_3":"docMetadata_3",
        "RDMPR7_4":"docMetadata_4",
        "RDMPR7_5":"docMetadata_5",
        "RDMPR7_6":"docMetadata_6",
        "RDMPR7_7":"docMetadata_7",
        "RDMPR7_8":"docMetadata_8",
        "RDMPR7_9":"docMetadata_9",
        "RDMPR7_other":"docMetadata_other",
        "RDMPR8_2":"docDigital_2",
        "RDMPR8_3":"docDigital_3",
        "RDMPR8_4":"docDigital_4",
        "RDMPR8_5":"docDigital_5",
        "RDMPR8_6":"docDigital_6",
        "RDMPR8_7":"docDigital_7",
        "RDMPR8_8":"docDigital_8",
        "RDMPR8_9":"docDigital_9",
        "RDMPR8_10":"docDigital_other",
        "RDMPR9_2":"docAuto_2",
        "RDMPR9_3":"docAuto_3",
        "RDMPR9_4":"docAuto_4",
        "RDMPR9_5":"docAuto_5",
        "RDMPR9_6":"docAuto_6",
        "RDMPR9_7":"docAuto_7",
        "RDMPR9_8":"docAuto_8",
        "RDMPR9_9":"docAuto_9",
        "RDMPR9_10":"docAuto_other",
        "RDMPR4":"docStructured",
        "RDMPR5":"docDefSchema",
        "DTPUB7_0":"pubMetadata_0",
        "DTPUB7_1":"pubMetadata_1",
        "DTPUB7_21":"pubMetadata_21",
        "DTPUB7_22":"pubMetadata_22",
        "DTPUB7_23":"pubMetadata_23",
        "DTPUB7_24":"pubMetadata_24",
        "DTPUB7_31":"pubMetadata_31",
        "DTPUB7_32":"pubMetadata_32",
        "DTPUB7_33":"pubMetadata_33",
        "DTPUB7_41":"pubMetadata_41",
        "DTPUB7_42":"pubMetadata_42",
        "DTPUB7_43":"pubMetadata_43",
        "DTPUB7_44":"pubMetadata_44",
        "DTPUB7_51":"pubMetadata_51",
        "DTPUB7_52":"pubMetadata_52",
        "DTPUB7_61":"pubMetadata_61",
        "DTPUB7_62":"pubMetadata_62",
        "DTPUB7_71":"pubMetadata_71",
        "DTPUB7_72":"pubMetadata_72",
        "DTPUB7_81":"pubMetadata_81",
        "DTPUB7_82":"pubMetadata_82",
        "DTPUB7_83":"pubMetadata_83",
        "DTPUB7_91":"pubMetadata_91",
        "DTPUB7_92":"pubMetadata_92",
        "DTPUB7_93":"pubMetadata_93",
        "DTPUB7_other":"pubMetadata_other",
        "RDMPR6_1":"docStandards_1",
        "RDMPR6_2":"docStandards_2",
        "RDMPR6_3":"docStandards_3",
        "RDMPR6_4":"docStandards_4",
        "RDMPR6_5":"docStandards_5",
        "RDMPR6_6":"docStandards_6",
        "RDMPR6_7":"docStandards_7",
        "RDMPR6_8":"docStandards_8",
        "RDMPR6_9":"docStandards_9",
        "RDMPR6_10":"docStandards_10",
        "RDMPR6_11":"docStandards_11",
        "RDMPR6_12":"docStandards_12",
        "RDMPR6_13":"docStandards_13",
        "RDMPR6_14":"docStandards_14",
        "RDMPR6_15":"docStandards_15",
        "RDMPR6_16":"docStandards_16",
        "RDMPR6_17":"docStandards_17",
        "RDMPR6_18":"docStandards_18",
        "RDMPR6_19":"docStandards_19",
        "RDMPR6_20":"docStandards_20",
        "RDMPR6_21":"docStandards_21",
        "RDMPR6_22":"docStandards_22",
        "RDMPR6_23":"docStandards_23",
        "RDMPR6_24":"docStandards_24",
        "RDMPR6_25":"docStandards_25",
        "RDMPR6_26":"docStandards_26",
        "RDMPR6_other":"docStandards_other",
        "RDMPR10_1":"software_1",
        "RDMPR10_2":"software_2",
        "RDMPR10_3":"software_3",
        "RDMPR12_0":"docMotivation_0",
        "RDMPR12_1":"docMotivation_1",
        "RDMPR12_2":"docMotivation_2",
        "RDMPR12_3":"docMotivation_3",
        "RDMPR12_4":"docMotivation_4",
        "RDMPR12_5":"docMotivation_5",
        "RDMPR12_6":"docMotivation_6",
        "RDMPR12_other":"docMotivation_other",
        "RDMPR11_0":"docObstacles_0",
        "RDMPR11_1":"docObstacles_1",
        "RDMPR11_2":"docObstacles_2",
        "RDMPR11_3":"docObstacles_3",
        "RDMPR11_4":"docObstacles_4",
        "RDMPR11_5":"docObstacles_5",
        "RDMPR11_6":"docObstacles_6",
        "RDMPR11_7":"docObstacles_7",
        "RDMPR11_8":"docObstacles_8",
        "RDMPR11_9":"docObstacles_9",
        "RDMPR11_other":"docObstacles_other",
        "SERVC1_0":"servNeeds_sub_0",
        "SERVC1_1":"servNeeds_sub_1",
        "SERVC1_2":"servNeeds_sub_2",
        "SERVC1_3":"servNeeds_sub_3",
        "SERVC1_4":"servNeeds_sub_4",
        "SERVC1_5":"servNeeds_sub_5",
        "SERVC1_6":"servNeeds_sub_6",
        "SERVC1_7":"servNeeds_sub_7",
        "SERVC1_8":"servNeeds_sub_8",
        "SERVC1_9":"servNeeds_sub_9",
        "SERVC1_other":"servNeeds_sub_other",
        "SERVC2_1":"servFormat_1",
        "SERVC2_2":"servFormat_2",
        "SERVC2_3":"servFormat_3",
        "SERVC2_4":"servFormat_4",
        "SERVC2_5":"servFormat_5",
        "SERVC2_6":"servFormat_6",
        "SERVC3":"feedback"
        }

##########################################
############### DICTIONARY ###############
###### DEFINE DATA TYPES OF COLUMNS ######
########################################## 

### for categorical, numerical and string answers

HCS_dtypesWOmc = {
        "centerAffiliation":"category",
        "researchFieldHGF":"category",
        "researchArea":"category",
        "researchAreaING":"category",
        "researchAreaGEO":"category",
        "researchAreaMATH":"category",
        "researchAreaPHYS":"category",
        "researchAreaLIFE":"category",
        "researchAreaBIO":"category",
        "researchAreaMED":"category",
        "researchAreaAGRI":"category",
        "researchAreaPSYCH":"category",
        "researchAreaCHEM":"category",
        "yearsInResearch":"category",
        "dataInPublication":"category",
        "pubAmount":"float64",
        "careerLevel":"category",
        "orcid":"category",
        "fairFamiliarity":"category",
        "dataOrigin_MeasVsSim":"category",
        "dataOrigin_SelvVsReuse":"category",
        "dataGatherTime":"float64",
        "experimentDuration_sub":"category",
        "dataAnalDuration_sub":"category",
        "longtermStorage":"category",
        "docStructured":"category",
        "docDefSchema":"category",
        "servFormat_1":"category",
        "servFormat_2":"category",
        "servFormat_3":"category",
        "servFormat_4":"category",
        "servFormat_5":"category",
        "servFormat_6":"category",
        "startlanguage":"category",
        "lastpage":"category"
        }


###############################################
#################### LIST #####################
###### SPECIFY MULTIPLE CHOICE QUESTIONS ######
############################################### 

# List  to specify all multiple choice questions
# For MC question cleaning
# List includes common strings of MC question column names

HCS_MCList = [
        "dataGenMethod_", 
        "lsfIdent_", 
        "dataFormats_", 
        "pubMethod_", 
        "pubMotivation_", 
        "pubObstacles_", 
        "pubMetadata_", 
        "pubStorage_", 
        "docMethod_", 
        "docMetadata_", 
        "docMotivation_", 
        "docStandards_", 
        "docObstacles_", 
        "servNeeds_sub_" 
        ]

##########################################
############### DICTIONARY ###############
########### CONVERT TO BOOLEAN ###########
##########################################

# Dictionary to convert MC answers to dtype = 'boolean'
# In this case, MC questions were exported with 'Yes'/'No' answers 

convertToBoolDict = {
        'Y':True,
        'N':False
        }

####################################################
#################### DICTIONARY ####################
########### ABBREVIATED HGF CENTER NAMES ###########
####################################################

# Dictionary to abbreviate center names in seperate column
# facilitates data handling

abbrevCenterAffilDict  = {
 'Alfred-Wegener-Institute (AWI)':"AWI",
 'Deutsches Elektronen-Synchrotron (DESY)':"DESY",
 'Forschungszentrum Jülich (FZJ)':"FZJ",
 'German Aerospace Center (DLR)':"DLR",
 'German Cancer Research Center (DKFZ)':"DKFZ",
 'German Center for Neurodegenerative Diseases (DZNE)':"DZNE",
 'German Research Centre for Geosciences (GFZ)':"GFZ",
 'Helmholtz Center for Information Security (CISPA)':"CISPA",
 'Helmholtz Centre for Environmental Research (UFZ)':"UFZ",
 'Helmholtz Centre for Heavy Ion Research (GSI)':"GSI",
 'Helmholtz Centre for Infection Research (HZI)':"HZI",
 'Helmholtz Centre for Ocean Research Kiel (GEOMAR)':"GEOMAR",
 'Helmholtz Zentrum München - German Research Center for Environmental Health (HMGU)':"HMGU",
 'Helmholtz-Zentrum Berlin für Materialien und Energie (HZB)':"HZB",
 'Helmholtz-Zentrum Dresden-Rossendorf (HZDR)':"HZDR",
 'Helmholtz-Zentrum Hereon':"Hereon",
 'Karlsruhe Institute of Technology (KIT)':"KIT",
 'Max Delbrück Center for Molecular Medicine in the Helmholtz Association (MDC)':"MDC",
 'Other':"Other"}


#######################################################
###################### DICTIONARY #####################
########### ABBREVIATED HGF RESEARCH FIELDS ###########
#######################################################

# Dictionary to abbreviate HGF research fields in seperate column
# abbreviated research Fields = HMC HUBS

abbrevHubsDict = {
    'Aeronautics, Space and Transportation':"AST",
    'Earth and Environment':"E&E",
    'Energy':"Energy",
    'Health':"Health",
    'Information':"Info",
    'Matter':"Matter"
        }


#######################################################
###################### DICTIONARY #####################
############## MULTIPLE CHOICE QUESTIONS ##############
##################### SUBQUESTIONS ####################
#######################################################

# Dictionary specifying the subquestions of multiple choice questions
 
HCS_MCsubquestions = {
        
        "dataFormats_":{"dataFormats_1":"archives",
                        "dataFormats_2":"audiovisual \n formats",
                        "dataFormats_3":"configurations",
                        "dataFormats_4":"databases",
                        "dataFormats_5":"images",
                        "dataFormats_6":"network-based data",
                        "dataFormats_7":"plain text",
                        "dataFormats_8":"device-specific \n data formats",
                        "dataFormats_9":"statistical \n data formats",
                        "dataFormats_10":"application-specific \n formats",
                        "dataFormats_11":"source code",
                        "dataFormats_12":"office applications",
                        "dataFormats_13":"structured graphics",
                        "dataFormats_14":"structured text",
                        "dataFormats_15":"binary scientific \n formats"
                        },
            
            "dataGenMethod_":{'dataGenMethod_1':"imaging",
                              'dataGenMethod_2':"analytical methods",
                              'dataGenMethod_3':"simulations",
                              'dataGenMethod_4':"sample synthesis \n and preparation",
                              'dataGenMethod_5':"cohort studies",
                              'dataGenMethod_6':"recordings"
                              },
                              
            "dataStorage_":{'dataStorage_0':"I don't know.", 
                            'dataStorage_1':"locally", 
                            'dataStorage_2':"centrally \n (internal server)",
                            'dataStorage_3':"externally \n (servers / repositories)"
                            },
                                                       
            "docMetadata_":{'docMetadata_2':"contextual information",
                            'docMetadata_3':"provenance of data",
                            'docMetadata_4':"information on data collection",
                            'docMetadata_5':"data processing and analysis",
                            'docMetadata_6':"description of data structure",
                            'docMetadata_7':"legal conditions",
                            'docMetadata_8':"information on storage \n and long-term preservation",
                            'docMetadata_9':"access information"
                            },
                         
            "docMethod_":{'docMethod_0':"no documentation", 
                          'docMethod_1':"pen and paper", 
                          'docMethod_2':"digital system", 
                          'docMethod_3':"digital text"
                          },
                         
            "docMotivation_":{'docMotivation_0':"no specific reason",
                              'docMotivation_1':"improved findability",
                              'docMotivation_2':"provide research \n data context",
                              'docMotivation_3':"improved reproducibility \n of workflows",
                              'docMotivation_4':"facilitate data publication",
                              'docMotivation_5':"scientific community \n recognition",
                              'docMotivation_6':"administrative guidelines"
                              },
                              
            "docObstacles_":{'docObstacles_0':"no difficulties",
                             'docObstacles_1':"lack of resources",
                             'docObstacles_4':"lack of incentives",
                             'docObstacles_5':"lack of technical knowledge",
                             'docObstacles_6':"lack of technical solutions",
                             'docObstacles_7':"legal / ethical inscurities",
                             'docObstacles_8':"no apparent benefits.",
                             'docObstacles_9':"lack of experience"
                            },
                             
            "docStandards_":{'docStandards_1':"DataCite",
                             'docStandards_10':"MiAIRR",
                             'docStandards_11':"MIBBI",
                             'docStandards_12':"MIABE",
                             'docStandards_13':"DDI",
                             'docStandards_14':"PREMIS",
                             'docStandards_15':"OEO",
                             'docStandards_16':"IEC standards",
                             'docStandards_17':"Brick",
                             'docStandards_18':"CityGML",
                             'docStandards_19':"IFC",
                             'docStandards_2':"Dublin Core",
                             'docStandards_20':"SSN / SOS",
                             'docStandards_21':"QUDT",
                             'docStandards_22':"NetCDF",
                             'docStandards_23':"SSN / SensorML",
                             'docStandards_24':"PROV-O",
                             'docStandards_25':"CIF",
                             'docStandards_26':"CSMD",
                             'docStandards_3':"DCAT",
                             'docStandards_4':"ISO-Standards",
                             'docStandards_5':"NeXus",
                             'docStandards_6':"MIAME",
                             'docStandards_7':"MINSEQ",
                             'docStandards_8':"MIxS",
                             'docStandards_9':"Darwin Core"
                             },
                             
            "lsfIdent_":{'lsfIdent_1':"LHC",
                         'lsfIdent_10':"SIS18",
                         'lsfIdent_11':"ESR",
                         'lsfIdent_2':"PETRA III",
                         'lsfIdent_3':"BESSY II",
                         'lsfIdent_4':"KATRIN",
                         'lsfIdent_5':"ELBE",
                         'lsfIdent_6':"BER II",
                         'lsfIdent_7':"FLASH",
                         'lsfIdent_8':"European XFEL",
                         'lsfIdent_9':"UNILAC"
                         },
                         
            "pubMetadata_":{'pubMetadata_0':"none",
                            'pubMetadata_1':"all of them",
                            'pubMetadata_21':"name of data set",
                            'pubMetadata_22':"(Persistent) Identifier",
                            'pubMetadata_23':"research subject",
                            'pubMetadata_24':"research method",
                            'pubMetadata_31':"author / producer of the data",
                            'pubMetadata_32':"acquisition location",
                            'pubMetadata_33':"collection data / period",
                            'pubMetadata_41':"devices used",
                            'pubMetadata_42':"device parameters used",
                            'pubMetadata_43':"data collection software",
                            'pubMetadata_44':"data collection workflows",
                            'pubMetadata_51':"analysis software / scripts",
                            'pubMetadata_52':"data analysis procedure",
                            'pubMetadata_61':"details on data formats",
                            'pubMetadata_62':"variable description",
                            'pubMetadata_71':"licensing information",
                            'pubMetadata_72':"access rights",
                            'pubMetadata_81':"retention period",
                            'pubMetadata_82':"backup strategies",
                            'pubMetadata_83':"sample storage conditions",
                            'pubMetadata_91':"API description",
                            'pubMetadata_92':"logs / statistics",
                            'pubMetadata_93':"registration procedures"
                            },
                            
            "pubMethod_":{'pubMethod_1':"supplementary to \n journal publication", 
                          'pubMethod_2':"in repository", 
                          'pubMethod_3':"data journal"
                          },
                          
            "pubMotivation_":{'pubMotivation_1':"reusability",
                              'pubMotivation_2':"visibility",
                              'pubMotivation_3':"publication statistics",
                              'pubMotivation_4':"gudelines / policies",
                              'pubMotivation_5':"good scientific practice",
                              'pubMotivation_6':"collaboration",
                              'pubMotivation_7':"financial benefits"
                              },
                              
            "pubObstaclesA_":{'pubObstaclesA_0':"no obstacles",    
                             'pubObstaclesA_1':"costs too high",
                             'pubObstaclesA_2':"lack of time / personnel",
                             'pubObstaclesA_3':"lack of incentives",
                             'pubObstaclesA_4':"possibility of data \n misinterpretation / misuse",
                             'pubObstaclesA_5':"technical barriers",
                             'pubObstaclesA_6':"legal / ethical concerns",
                             'pubObstaclesA_7':"technical support needed"
                             },
                              
            "pubObstaclesB_":{'pubObstaclesB_0':"no data to publish",
                              'pubObstaclesB_1':"costs too high",
                              'pubObstaclesB_2':"lack of time / personnel",
                              'pubObstaclesB_3':"lack of incentives",
                              'pubObstaclesB_4':"possibility of data \n misinterpretation / misuse",
                              'pubObstaclesB_5':"technical barriers",
                              'pubObstaclesB_6':"legal / ethical concerns",
                              'pubObstaclesB_7':"technical support needed"
                              }, 
            
            "servNeeds_sub_":{'servNeeds_sub_0':"no need for support",
                              'servNeeds_sub_1':"data publication",
                              'servNeeds_sub_2':"research data reuse",
                              'servNeeds_sub_3':"DMP development",
                              'servNeeds_sub_4':"metadata enrichment \n of research data",
                              'servNeeds_sub_5':"RDM software & tools",
                              'servNeeds_sub_6':"metadata use & analysis",
                              'servNeeds_sub_7':"legal aspects",
                              'servNeeds_sub_8':"best practices",
                              'servNeeds_sub_9':"technical aspects of RDM"
                              }
        }



#######################################################
###################### DICTIONARY #####################
############## ORDERED CATEGORICAL VALUES #############
#######################################################

HCS_orderedCats = {
        "yearsInResearch":['I do not have a Master\'s or diploma degree, yet', 
                           'Less than 1 year', 
                           '1 to 3 years', 
                           '4 to 6 years', 
                           '7 to 10 years', 
                           'More than 10 years'],
                   
        "careerLevel":['Undergraduate / Masters student', 
                       'PhD student', 'Postdoc', 
                       'Research associate', 
                       'Principal Investigator', 
                       'Director (of the institute)', 
                       'Other'],
                       
        "dataInPublication":['< 100 MB',
                             '100 MB - 1000 MB (1 GB)', 
                             '1 GB - 10 GB', 
                             '10 GB - 100 GB', 
                             '100 GB - 1000 GB (1 TB)',
                             '> 1 TB',
                             'I don\'t know.'],

        "experimentDuration_sub":['Less', 
                                  'As much', 
                                  'More', 
                                  'I don\'t know.'],
                                  
        
        "dataAnalDuration_sub":['Less', 
                                  'As much', 
                                  'More', 
                                  'I don\'t know.']
        }



HCSquestions = {
                "EN" : {        
                        "PERBG1":"Which Helmholtz center do you typically work in?",
                        "PERBG2":"Please select the Helmholtz research field you associate yourself with.",
                        "PERBG3":"Please select your principle research area.",
                        "PERBG4":"How many years have you been working in research?",
                        "PERBG6":"Which is your current career level?",
                        "PERBG7":"Do you have an ORCID iD?",
                        "PERBG8":"How familiar are you with the FAIR data guidelines?",
                        "RSDP1":"Please characterize the origin of your research data.",
                        "RSDP1b":"Which amount of your data sets was recorded at large scale facilities (e.g., LHC, PETRA III, KATRIN, ELBE, BESSY II)? (Percentage)",
                        "RSDP1c":"Please specify the large scale facility used:",
                        "RSDP2":"Please select the methods used to generate your research data.",
                        "RSDP2b":"Please specify the methods used to generate your research data.",
                        "RSDP3":"Please select the data formats that you generate or use in your current research project.",
                        "RSDP7":"Please estimate the amount of data a typical publication of yours is based on.",
                        "RSDP4":"What is the average time from planning to completion of data collection for your research projects? (in months)",
                        "RSDP8":"My experiments take ___ time than an average investigation in my research domain.",
                        "RSDP11":"My data analyses take ___ time than an average investigation in my research domain.",
                        "RSDP10":"Do you keep your unpublished raw data in long-term storage (10 years or longer)?",
                        "DTPUB6":"Please estimate the relative amount of your data sets that you make publicly available. (Percentage)",
                        "DTPUB1b":"How did you publish your data?",
                        "DTPUB5":"In which repositories have you published your data?",
                        "DTPUB3":"Which of the following motivated you to publish your data? (Please choose up to 3 options)",
                        "DTPUB4a":"What obstacles have you encountered in publishing your research data?",
                        "DTPUB4b":"What concerns or obstacles have discouraged you from publishing your research data so far?",
                        "RDMPR1":"Where is most of your research data stored after a project is finished?",
                        "RDMPR3":"In your current project, where do you document the steps used to generate and process your data?",
                        "RDMPR7":"Please select which information (metadata) you typically use to describe your research data?",
                        "RDMPR8":"Which information (metadata) do you typically document in a digital way?",
                        "RDMPR9":"Which of those information (metadata) do you typically gather in an automated way?",
                        "RDMPR4":"Do you document your research data in a structured way? (e.g., using forms, templates or schemas)",
                        "RDMPR5":"Do you use internationally used templates, schemas or standards for this purpose?",
                        "DTPUB7":"Which of these metadata do you publish along with your research data?",
                        "RDMPR6":"Which international standards do you use?",
                        "RDMPR10":"Please name the three most important software applications that you use for your research.",
                        "RDMPR12":"Which of these reasons motivates you to document your work in a structured way?",
                        "RDMPR11":"What obstacles or difficulties have you encountered in collecting metadata as part of your work?",
                        "SERVC1":"In which areas of research data management do you perceive a need for supporting services?",
                        "SERVC2":"Please rate your interest in the following service formats.",
                        "SERVC3":"You are almost there! You are welcome to formulate questions, wishes or suggestions in the following free text field:"
                        },
                "DE" : {
                        "PERBG1":"In welchem Helmholtz-Zentrum sind Sie in erster Linie tätig?",
                        "PERBG2":"Welchem Helmholtz-Forschungsbereich ordnen Sie sich am ehesten zu?",
                        "PERBG3":"Welcher Forschungsdisziplin ordnen Sie sich am ehesten zu?",
                        "PERBG4":"Wie viele Jahre sind Sie bereits in der Forschung tätig?",
                        "PERBG6":"Was ist Ihre aktuelle Position?",
                        "PERBG7":"Haben Sie eine ORCID iD?",
                        "PERBG8":"Wie vertraut sind Sie mit den FAIR-Data Leitlinien?",
                        "RSDP1":"Bitte charakterisieren Sie den Ursprung Ihrer Forschungsdaten.",
                        "RSDP1b":"Welcher Anteil Ihrer Datensätze wurde an Großforschungsanlagen (z.B. LHC, PETRA III, KATRIN ELBE, BESSY II) erfasst? (Angabe in Prozent)",
                        "RSDP1c":"Bitte nennen Sie die genutzte Großforschungseinrichtung:",
                        "RSDP2":"Mit welchen Methoden erheben Sie Ihre Forschungsdaten?",
                        "RSDP2b":"Bitte spezifizieren Sie die Methoden, mit denen Sie Ihre Forschungsdaten erheben.",
                        "RSDP3":"In welchen Datenformaten liegen die Daten vor, die Sie in Ihrem aktuellen Forschungsprojekt generieren bzw. nutzen?",
                        "RSDP7":"Bitte schätzen Sie, auf welcher Datenmenge eine typische Veröffentlichung von Ihnen beruht.",
                        "RSDP4":"Wie viel Zeit vergeht durchschnittlich von der Planung bis zum Abschluss der Datenaufnahme für Ihre Forschungsprojekte? (in Monaten)",
                        "RSDP8":"Meine Experimente nehmen ___ Zeit in Anspruch als eine durchnittliche Untersuchung in meinem Forschungsbereich.",
                        "RSDP11":"Meine Datenanalysen nehmen ___ Zeit in Anspruch als eine durchschnittliche Untersuchung in meinem Forschungsbereich.",
                        "RSDP10":"Speichern Sie Rohdaten, die nicht publiziert werden, langfristig (10 Jahre und länger)?",
                        "DTPUB6":"Bitte schätzen Sie, welchen relativen Anteil Ihrer Datensätze Sie publizieren. (Angabe in Prozent)",
                        "DTPUB1b":"Wie haben Sie Ihre Daten publiziert?",
                        "DTPUB5":"In welchen Repositorien haben Sie Ihre Daten veröffentlicht?",
                        "DTPUB3":"Was motivierte Sie dazu, Ihre Forschungsdaten zu veröffentlichen? (Bitte wählen Sie bis zu 3 Antworten)",
                        "DTPUB4a":"Auf welche Hindernisse sind Sie bei der Veröffentlichung Ihrer Forschungsdaten gestoßen?",
                        "DTPUB4b":"Welche Bedenken oder Hindernisse haben Sie bisher davon abgehalten, Ihre Forschungsdaten zu veröffentlichen?",
                        "RDMPR1":"Wo werden Ihre Forschungsdaten nach Abschluss eine Projekts hauptsächlich gespeichert?",
                        "RDMPR3":"Wo dokumentieren Sie in Ihrem aktuellen Projekt die Arbeitsschritte, mit denen Ihre Daten erzeugt und verarbeitet werden?",
                        "RDMPR7":"Mit welchen Informationen (Metadaten) beschreiben Sie normalerweise Ihre Forschungsdaten?",
                        "RDMPR8":"Welche Informationen (Metadaten) davon erfassen Sie in der Regel digital?",
                        "RDMPR9":"Welche dieser Informationen (Metadaten) erfassen Sie in der Regel automatisiert?",
                        "RDMPR4":"Dokumentieren Sie Ihre Forschungsdaten auf strukturierte Weise? (z.B. mittels Formularen, Vorlagen oder Schemata)",
                        "RDMPR5":"Verwenden Sie hierzu international genutzte Formulare, Schemata oder Standards?",
                        "DTPUB7":"Welche dieser Metadaten publizieren Sie zusammen mit Ihren Forschungsdaten?",
                        "RDMPR6":"Welche internationalen Standards nutzen Sie?",
                        "RDMPR10":"Bitte nennen Sie die drei wichtigsten Softwareanwendungen, die Sie für Ihre Forschung verwenden.",
                        "RDMPR12":"Was motiviert Sie dazu, Ihre Arbeitsschritte auf strukturierte Weise zu dokumentieren?",
                        "RDMPR11":"Auf welche Hindernisse oder Schwierigkeiten sind Sie bei der Erfassung von Metadaten im Rahmen Ihrer Arbeit gestoßen?",
                        "SERVC1":"In welchen Bereichen des Forschungsdatenmanagements haben Sie Bedarf an unterstützenden Angeboten?",
                        "SERVC2":"Bitte bewerten Sie Ihr Interesse an den folgenden Service-Formaten.",
                        "SERVC3":"Sie haben es fast geschafft! Gerne können Sie Fragen, Wünsche oder Anregungen im folgenden Freitextfeld formulieren:"
                        }
                    }

