#################################
# packages
#################################

import xarray as xr
import numpy as np
import matplotlib.pyplot as plt

from functools import reduce

#################################
## Determining common members
#################################
# Current predictors available
# performance fields: tos, swcre, pr, tas, psl, ECS
# independence fields: tas, psl
# spread fields: tas, pr

# members available for each predictor, CMIP6
CMIP6_tos_members = ['ACCESS-CM2-r1i1p1f1', 'ACCESS-CM2-r2i1p1f1',
       'ACCESS-CM2-r3i1p1f1', 'ACCESS-ESM1-5-r10i1p1f1',
       'ACCESS-ESM1-5-r1i1p1f1', 'ACCESS-ESM1-5-r2i1p1f1',
       'ACCESS-ESM1-5-r3i1p1f1', 'ACCESS-ESM1-5-r4i1p1f1',
       'ACCESS-ESM1-5-r5i1p1f1', 'ACCESS-ESM1-5-r6i1p1f1',
       'ACCESS-ESM1-5-r7i1p1f1', 'ACCESS-ESM1-5-r8i1p1f1',
       'ACCESS-ESM1-5-r9i1p1f1', 'AWI-CM-1-1-MR-r1i1p1f1',
       'BCC-CSM2-MR-r1i1p1f1', 'CAS-ESM2-0-r1i1p1f1',
       'CAS-ESM2-0-r3i1p1f1', 'CESM2-WACCM-r1i1p1f1',
       'CESM2-WACCM-r2i1p1f1', 'CESM2-WACCM-r3i1p1f1', 'CESM2-r10i1p1f1',
       'CESM2-r11i1p1f1', 'CESM2-r1i1p1f1', 'CESM2-r2i1p1f1',
       'CESM2-r4i1p1f1', 'CMCC-CM2-SR5-r1i1p1f1', 'CMCC-ESM2-r1i1p1f1',
       'CNRM-CM6-1-HR-r1i1p1f2', 'CNRM-CM6-1-r1i1p1f2',
       'CNRM-CM6-1-r2i1p1f2', 'CNRM-CM6-1-r3i1p1f2',
       'CNRM-CM6-1-r4i1p1f2', 'CNRM-CM6-1-r5i1p1f2',
       'CNRM-CM6-1-r6i1p1f2', 'CNRM-ESM2-1-r1i1p1f2',
       'CNRM-ESM2-1-r2i1p1f2', 'CNRM-ESM2-1-r3i1p1f2',
       'CNRM-ESM2-1-r4i1p1f2', 'CNRM-ESM2-1-r5i1p1f2',
       'CanESM5-r10i1p1f1', 'CanESM5-r10i1p2f1', 'CanESM5-r11i1p1f1',
       'CanESM5-r11i1p2f1', 'CanESM5-r12i1p1f1', 'CanESM5-r12i1p2f1',
       'CanESM5-r13i1p1f1', 'CanESM5-r13i1p2f1', 'CanESM5-r14i1p1f1',
       'CanESM5-r14i1p2f1', 'CanESM5-r15i1p1f1', 'CanESM5-r15i1p2f1',
       'CanESM5-r16i1p1f1', 'CanESM5-r16i1p2f1', 'CanESM5-r17i1p1f1',
       'CanESM5-r17i1p2f1', 'CanESM5-r18i1p1f1', 'CanESM5-r18i1p2f1',
       'CanESM5-r19i1p1f1', 'CanESM5-r19i1p2f1', 'CanESM5-r1i1p1f1',
       'CanESM5-r1i1p2f1', 'CanESM5-r20i1p1f1', 'CanESM5-r20i1p2f1',
       'CanESM5-r21i1p1f1', 'CanESM5-r21i1p2f1', 'CanESM5-r22i1p1f1',
       'CanESM5-r22i1p2f1', 'CanESM5-r23i1p1f1', 'CanESM5-r23i1p2f1',
       'CanESM5-r24i1p1f1', 'CanESM5-r24i1p2f1', 'CanESM5-r25i1p1f1',
       'CanESM5-r25i1p2f1', 'CanESM5-r2i1p1f1', 'CanESM5-r2i1p2f1',
       'CanESM5-r3i1p1f1', 'CanESM5-r3i1p2f1', 'CanESM5-r4i1p1f1',
       'CanESM5-r4i1p2f1', 'CanESM5-r5i1p1f1', 'CanESM5-r5i1p2f1',
       'CanESM5-r6i1p1f1', 'CanESM5-r6i1p2f1', 'CanESM5-r7i1p1f1',
       'CanESM5-r7i1p2f1', 'CanESM5-r8i1p1f1', 'CanESM5-r8i1p2f1',
       'CanESM5-r9i1p1f1', 'CanESM5-r9i1p2f1', 'E3SM-1-1-r1i1p1f1',
       'EC-Earth3-Veg-r1i1p1f1', 'EC-Earth3-Veg-r2i1p1f1',
       'EC-Earth3-Veg-r3i1p1f1', 'EC-Earth3-Veg-r4i1p1f1',
       'EC-Earth3-Veg-r6i1p1f1', 'EC-Earth3-r11i1p1f1',
       'EC-Earth3-r13i1p1f1', 'EC-Earth3-r15i1p1f1', 'EC-Earth3-r1i1p1f1',
       'EC-Earth3-r3i1p1f1', 'EC-Earth3-r4i1p1f1', 'EC-Earth3-r6i1p1f1',
       'EC-Earth3-r9i1p1f1', 'FGOALS-f3-L-r1i1p1f1',
       'FGOALS-f3-L-r2i1p1f1', 'FGOALS-f3-L-r3i1p1f1',
       'FGOALS-g3-r1i1p1f1', 'FGOALS-g3-r2i1p1f1', 'FIO-ESM-2-0-r1i1p1f1',
       'FIO-ESM-2-0-r2i1p1f1', 'FIO-ESM-2-0-r3i1p1f1',
       'GFDL-CM4-r1i1p1f1', 'GFDL-ESM4-r1i1p1f1', 'GISS-E2-1-G-r1i1p1f2',
       'GISS-E2-1-G-r1i1p3f1', 'HadGEM3-GC31-LL-r1i1p1f3',
       'HadGEM3-GC31-LL-r2i1p1f3', 'HadGEM3-GC31-LL-r3i1p1f3',
       'HadGEM3-GC31-LL-r4i1p1f3', 'HadGEM3-GC31-MM-r1i1p1f3',
       'HadGEM3-GC31-MM-r2i1p1f3', 'HadGEM3-GC31-MM-r3i1p1f3',
       'HadGEM3-GC31-MM-r4i1p1f3', 'INM-CM4-8-r1i1p1f1',
       'INM-CM5-0-r1i1p1f1', 'IPSL-CM6A-LR-r14i1p1f1',
       'IPSL-CM6A-LR-r1i1p1f1', 'IPSL-CM6A-LR-r2i1p1f1',
       'IPSL-CM6A-LR-r3i1p1f1', 'IPSL-CM6A-LR-r4i1p1f1',
       'IPSL-CM6A-LR-r6i1p1f1', 'KACE-1-0-G-r2i1p1f1',
       'KACE-1-0-G-r3i1p1f1', 'KIOST-ESM-r1i1p1f1', 'MCM-UA-1-0-r1i1p1f2',
       'MIROC-ES2L-r10i1p1f2', 'MIROC-ES2L-r1i1p1f2',
       'MIROC-ES2L-r2i1p1f2', 'MIROC-ES2L-r3i1p1f2',
       'MIROC-ES2L-r4i1p1f2', 'MIROC-ES2L-r5i1p1f2',
       'MIROC-ES2L-r6i1p1f2', 'MIROC-ES2L-r7i1p1f2',
       'MIROC-ES2L-r8i1p1f2', 'MIROC-ES2L-r9i1p1f2', 'MIROC6-r10i1p1f1',
       'MIROC6-r11i1p1f1', 'MIROC6-r12i1p1f1', 'MIROC6-r13i1p1f1',
       'MIROC6-r14i1p1f1', 'MIROC6-r15i1p1f1', 'MIROC6-r16i1p1f1',
       'MIROC6-r17i1p1f1', 'MIROC6-r18i1p1f1', 'MIROC6-r19i1p1f1',
       'MIROC6-r1i1p1f1', 'MIROC6-r20i1p1f1', 'MIROC6-r21i1p1f1',
       'MIROC6-r22i1p1f1', 'MIROC6-r23i1p1f1', 'MIROC6-r24i1p1f1',
       'MIROC6-r25i1p1f1', 'MIROC6-r26i1p1f1', 'MIROC6-r27i1p1f1',
       'MIROC6-r28i1p1f1', 'MIROC6-r29i1p1f1', 'MIROC6-r2i1p1f1',
       'MIROC6-r30i1p1f1', 'MIROC6-r31i1p1f1', 'MIROC6-r32i1p1f1',
       'MIROC6-r33i1p1f1', 'MIROC6-r34i1p1f1', 'MIROC6-r35i1p1f1',
       'MIROC6-r36i1p1f1', 'MIROC6-r37i1p1f1', 'MIROC6-r38i1p1f1',
       'MIROC6-r39i1p1f1', 'MIROC6-r3i1p1f1', 'MIROC6-r40i1p1f1',
       'MIROC6-r41i1p1f1', 'MIROC6-r42i1p1f1', 'MIROC6-r43i1p1f1',
       'MIROC6-r44i1p1f1', 'MIROC6-r45i1p1f1', 'MIROC6-r46i1p1f1',
       'MIROC6-r47i1p1f1', 'MIROC6-r48i1p1f1', 'MIROC6-r49i1p1f1',
       'MIROC6-r4i1p1f1', 'MIROC6-r50i1p1f1', 'MIROC6-r5i1p1f1',
       'MIROC6-r6i1p1f1', 'MIROC6-r7i1p1f1', 'MIROC6-r8i1p1f1',
       'MIROC6-r9i1p1f1', 'MPI-ESM1-2-HR-r1i1p1f1',
       'MPI-ESM1-2-HR-r2i1p1f1', 'MPI-ESM1-2-LR-r10i1p1f1',
       'MPI-ESM1-2-LR-r1i1p1f1', 'MPI-ESM1-2-LR-r2i1p1f1',
       'MPI-ESM1-2-LR-r3i1p1f1', 'MPI-ESM1-2-LR-r4i1p1f1',
       'MPI-ESM1-2-LR-r5i1p1f1', 'MPI-ESM1-2-LR-r6i1p1f1',
       'MPI-ESM1-2-LR-r7i1p1f1', 'MPI-ESM1-2-LR-r8i1p1f1',
       'MPI-ESM1-2-LR-r9i1p1f1', 'MRI-ESM2-0-r1i1p1f1',
       'MRI-ESM2-0-r1i2p1f1', 'NESM3-r1i1p1f1', 'NESM3-r2i1p1f1',
       'NorESM2-LM-r1i1p1f1', 'NorESM2-MM-r1i1p1f1', 'TaiESM1-r1i1p1f1',
       'UKESM1-0-LL-r1i1p1f2', 'UKESM1-0-LL-r2i1p1f2',
       'UKESM1-0-LL-r3i1p1f2', 'UKESM1-0-LL-r4i1p1f2',
       'UKESM1-0-LL-r8i1p1f2']

CMIP6_swcre_members = ['ACCESS-CM2-r1i1p1f1', 'ACCESS-CM2-r2i1p1f1',
       'ACCESS-CM2-r3i1p1f1', 'ACCESS-ESM1-5-r10i1p1f1',
       'ACCESS-ESM1-5-r1i1p1f1', 'ACCESS-ESM1-5-r2i1p1f1',
       'ACCESS-ESM1-5-r3i1p1f1', 'ACCESS-ESM1-5-r4i1p1f1',
       'ACCESS-ESM1-5-r5i1p1f1', 'ACCESS-ESM1-5-r6i1p1f1',
       'ACCESS-ESM1-5-r7i1p1f1', 'ACCESS-ESM1-5-r8i1p1f1',
       'ACCESS-ESM1-5-r9i1p1f1', 'AWI-CM-1-1-MR-r1i1p1f1',
       'BCC-CSM2-MR-r1i1p1f1', 'CAS-ESM2-0-r1i1p1f1',
       'CAS-ESM2-0-r3i1p1f1', 'CESM2-WACCM-r1i1p1f1',
       'CESM2-WACCM-r2i1p1f1', 'CESM2-WACCM-r3i1p1f1', 'CESM2-r10i1p1f1',
       'CESM2-r11i1p1f1', 'CESM2-r1i1p1f1', 'CESM2-r2i1p1f1',
       'CESM2-r4i1p1f1', 'CIESM-r1i1p1f1', 'CMCC-CM2-SR5-r1i1p1f1',
       'CMCC-ESM2-r1i1p1f1', 'CNRM-CM6-1-HR-r1i1p1f2',
       'CNRM-CM6-1-r1i1p1f2', 'CNRM-CM6-1-r2i1p1f2',
       'CNRM-CM6-1-r3i1p1f2', 'CNRM-CM6-1-r4i1p1f2',
       'CNRM-CM6-1-r5i1p1f2', 'CNRM-CM6-1-r6i1p1f2',
       'CNRM-ESM2-1-r1i1p1f2', 'CNRM-ESM2-1-r2i1p1f2',
       'CNRM-ESM2-1-r3i1p1f2', 'CNRM-ESM2-1-r4i1p1f2',
       'CNRM-ESM2-1-r5i1p1f2', 'CanESM5-r10i1p1f1', 'CanESM5-r10i1p2f1',
       'CanESM5-r11i1p1f1', 'CanESM5-r11i1p2f1', 'CanESM5-r12i1p1f1',
       'CanESM5-r12i1p2f1', 'CanESM5-r13i1p1f1', 'CanESM5-r13i1p2f1',
       'CanESM5-r14i1p1f1', 'CanESM5-r14i1p2f1', 'CanESM5-r15i1p1f1',
       'CanESM5-r15i1p2f1', 'CanESM5-r16i1p1f1', 'CanESM5-r16i1p2f1',
       'CanESM5-r17i1p1f1', 'CanESM5-r17i1p2f1', 'CanESM5-r18i1p1f1',
       'CanESM5-r18i1p2f1', 'CanESM5-r19i1p1f1', 'CanESM5-r19i1p2f1',
       'CanESM5-r1i1p1f1', 'CanESM5-r1i1p2f1', 'CanESM5-r20i1p1f1',
       'CanESM5-r20i1p2f1', 'CanESM5-r21i1p1f1', 'CanESM5-r21i1p2f1',
       'CanESM5-r22i1p1f1', 'CanESM5-r22i1p2f1', 'CanESM5-r23i1p1f1',
       'CanESM5-r23i1p2f1', 'CanESM5-r24i1p1f1', 'CanESM5-r24i1p2f1',
       'CanESM5-r25i1p1f1', 'CanESM5-r25i1p2f1', 'CanESM5-r2i1p1f1',
       'CanESM5-r2i1p2f1', 'CanESM5-r3i1p1f1', 'CanESM5-r3i1p2f1',
       'CanESM5-r4i1p1f1', 'CanESM5-r4i1p2f1', 'CanESM5-r5i1p1f1',
       'CanESM5-r5i1p2f1', 'CanESM5-r6i1p1f1', 'CanESM5-r6i1p2f1',
       'CanESM5-r7i1p1f1', 'CanESM5-r7i1p2f1', 'CanESM5-r8i1p1f1',
       'CanESM5-r8i1p2f1', 'CanESM5-r9i1p1f1', 'CanESM5-r9i1p2f1',
       'E3SM-1-1-r1i1p1f1', 'FGOALS-f3-L-r1i1p1f1', 'FGOALS-g3-r1i1p1f1',
       'FGOALS-g3-r2i1p1f1', 'FGOALS-g3-r3i1p1f1', 'FGOALS-g3-r4i1p1f1',
       'FIO-ESM-2-0-r1i1p1f1', 'FIO-ESM-2-0-r2i1p1f1',
       'FIO-ESM-2-0-r3i1p1f1', 'GFDL-CM4-r1i1p1f1', 'GFDL-ESM4-r1i1p1f1',
       'GISS-E2-1-G-r1i1p3f1', 'GISS-E2-1-G-r1i1p5f1',
       'GISS-E2-1-G-r2i1p3f1', 'GISS-E2-1-G-r3i1p3f1',
       'GISS-E2-1-G-r4i1p3f1', 'GISS-E2-1-G-r5i1p3f1',
       'HadGEM3-GC31-LL-r1i1p1f3', 'HadGEM3-GC31-LL-r2i1p1f3',
       'HadGEM3-GC31-LL-r3i1p1f3', 'HadGEM3-GC31-LL-r4i1p1f3',
       'HadGEM3-GC31-MM-r1i1p1f3', 'HadGEM3-GC31-MM-r2i1p1f3',
       'HadGEM3-GC31-MM-r3i1p1f3', 'HadGEM3-GC31-MM-r4i1p1f3',
       'INM-CM4-8-r1i1p1f1', 'INM-CM5-0-r1i1p1f1',
       'IPSL-CM6A-LR-r14i1p1f1', 'IPSL-CM6A-LR-r1i1p1f1',
       'IPSL-CM6A-LR-r2i1p1f1', 'IPSL-CM6A-LR-r3i1p1f1',
       'IPSL-CM6A-LR-r4i1p1f1', 'IPSL-CM6A-LR-r6i1p1f1',
       'KACE-1-0-G-r1i1p1f1', 'KACE-1-0-G-r2i1p1f1',
       'KACE-1-0-G-r3i1p1f1', 'KIOST-ESM-r1i1p1f1',
       'MIROC-ES2L-r10i1p1f2', 'MIROC-ES2L-r1i1p1f2',
       'MIROC-ES2L-r2i1p1f2', 'MIROC-ES2L-r3i1p1f2',
       'MIROC-ES2L-r4i1p1f2', 'MIROC-ES2L-r5i1p1f2',
       'MIROC-ES2L-r6i1p1f2', 'MIROC-ES2L-r7i1p1f2',
       'MIROC-ES2L-r8i1p1f2', 'MIROC-ES2L-r9i1p1f2', 'MIROC6-r10i1p1f1',
       'MIROC6-r11i1p1f1', 'MIROC6-r12i1p1f1', 'MIROC6-r13i1p1f1',
       'MIROC6-r14i1p1f1', 'MIROC6-r15i1p1f1', 'MIROC6-r16i1p1f1',
       'MIROC6-r17i1p1f1', 'MIROC6-r18i1p1f1', 'MIROC6-r19i1p1f1',
       'MIROC6-r1i1p1f1', 'MIROC6-r20i1p1f1', 'MIROC6-r21i1p1f1',
       'MIROC6-r22i1p1f1', 'MIROC6-r23i1p1f1', 'MIROC6-r24i1p1f1',
       'MIROC6-r25i1p1f1', 'MIROC6-r26i1p1f1', 'MIROC6-r27i1p1f1',
       'MIROC6-r28i1p1f1', 'MIROC6-r29i1p1f1', 'MIROC6-r2i1p1f1',
       'MIROC6-r30i1p1f1', 'MIROC6-r31i1p1f1', 'MIROC6-r32i1p1f1',
       'MIROC6-r33i1p1f1', 'MIROC6-r34i1p1f1', 'MIROC6-r35i1p1f1',
       'MIROC6-r36i1p1f1', 'MIROC6-r37i1p1f1', 'MIROC6-r38i1p1f1',
       'MIROC6-r39i1p1f1', 'MIROC6-r3i1p1f1', 'MIROC6-r40i1p1f1',
       'MIROC6-r41i1p1f1', 'MIROC6-r42i1p1f1', 'MIROC6-r43i1p1f1',
       'MIROC6-r44i1p1f1', 'MIROC6-r45i1p1f1', 'MIROC6-r46i1p1f1',
       'MIROC6-r47i1p1f1', 'MIROC6-r48i1p1f1', 'MIROC6-r49i1p1f1',
       'MIROC6-r4i1p1f1', 'MIROC6-r50i1p1f1', 'MIROC6-r5i1p1f1',
       'MIROC6-r6i1p1f1', 'MIROC6-r7i1p1f1', 'MIROC6-r8i1p1f1',
       'MIROC6-r9i1p1f1', 'MPI-ESM1-2-HR-r1i1p1f1',
       'MPI-ESM1-2-HR-r2i1p1f1', 'MPI-ESM1-2-LR-r10i1p1f1',
       'MPI-ESM1-2-LR-r1i1p1f1', 'MPI-ESM1-2-LR-r2i1p1f1',
       'MPI-ESM1-2-LR-r3i1p1f1', 'MPI-ESM1-2-LR-r4i1p1f1',
       'MPI-ESM1-2-LR-r5i1p1f1', 'MPI-ESM1-2-LR-r6i1p1f1',
       'MPI-ESM1-2-LR-r7i1p1f1', 'MPI-ESM1-2-LR-r8i1p1f1',
       'MPI-ESM1-2-LR-r9i1p1f1', 'MRI-ESM2-0-r1i1p1f1',
       'MRI-ESM2-0-r1i2p1f1', 'NESM3-r1i1p1f1', 'NESM3-r2i1p1f1',
       'NorESM2-LM-r1i1p1f1', 'NorESM2-MM-r1i1p1f1', 'TaiESM1-r1i1p1f1',
       'UKESM1-0-LL-r1i1p1f2', 'UKESM1-0-LL-r2i1p1f2',
       'UKESM1-0-LL-r3i1p1f2', 'UKESM1-0-LL-r4i1p1f2',
       'UKESM1-0-LL-r8i1p1f2']

CMIP6_pr_members = ['ACCESS-CM2-r1i1p1f1', 'ACCESS-CM2-r2i1p1f1',
       'ACCESS-CM2-r3i1p1f1', 'ACCESS-ESM1-5-r10i1p1f1',
       'ACCESS-ESM1-5-r1i1p1f1', 'ACCESS-ESM1-5-r2i1p1f1',
       'ACCESS-ESM1-5-r3i1p1f1', 'ACCESS-ESM1-5-r4i1p1f1',
       'ACCESS-ESM1-5-r5i1p1f1', 'ACCESS-ESM1-5-r6i1p1f1',
       'ACCESS-ESM1-5-r7i1p1f1', 'ACCESS-ESM1-5-r8i1p1f1',
       'ACCESS-ESM1-5-r9i1p1f1', 'AWI-CM-1-1-MR-r1i1p1f1',
       'BCC-CSM2-MR-r1i1p1f1', 'CAS-ESM2-0-r1i1p1f1',
       'CAS-ESM2-0-r3i1p1f1', 'CESM2-WACCM-r1i1p1f1',
       'CESM2-WACCM-r2i1p1f1', 'CESM2-WACCM-r3i1p1f1', 'CESM2-r10i1p1f1',
       'CESM2-r11i1p1f1', 'CESM2-r1i1p1f1', 'CESM2-r2i1p1f1',
       'CESM2-r4i1p1f1', 'CIESM-r1i1p1f1', 'CMCC-CM2-SR5-r1i1p1f1',
       'CMCC-ESM2-r1i1p1f1', 'CNRM-CM6-1-HR-r1i1p1f2',
       'CNRM-CM6-1-r1i1p1f2', 'CNRM-CM6-1-r2i1p1f2',
       'CNRM-CM6-1-r3i1p1f2', 'CNRM-CM6-1-r4i1p1f2',
       'CNRM-CM6-1-r5i1p1f2', 'CNRM-CM6-1-r6i1p1f2',
       'CNRM-ESM2-1-r1i1p1f2', 'CNRM-ESM2-1-r2i1p1f2',
       'CNRM-ESM2-1-r3i1p1f2', 'CNRM-ESM2-1-r4i1p1f2',
       'CNRM-ESM2-1-r5i1p1f2', 'CanESM5-r10i1p1f1', 'CanESM5-r10i1p2f1',
       'CanESM5-r11i1p1f1', 'CanESM5-r11i1p2f1', 'CanESM5-r12i1p1f1',
       'CanESM5-r12i1p2f1', 'CanESM5-r13i1p1f1', 'CanESM5-r13i1p2f1',
       'CanESM5-r14i1p1f1', 'CanESM5-r14i1p2f1', 'CanESM5-r15i1p1f1',
       'CanESM5-r15i1p2f1', 'CanESM5-r16i1p1f1', 'CanESM5-r16i1p2f1',
       'CanESM5-r17i1p1f1', 'CanESM5-r17i1p2f1', 'CanESM5-r18i1p1f1',
       'CanESM5-r18i1p2f1', 'CanESM5-r19i1p1f1', 'CanESM5-r19i1p2f1',
       'CanESM5-r1i1p1f1', 'CanESM5-r1i1p2f1', 'CanESM5-r20i1p1f1',
       'CanESM5-r20i1p2f1', 'CanESM5-r21i1p1f1', 'CanESM5-r21i1p2f1',
       'CanESM5-r22i1p1f1', 'CanESM5-r22i1p2f1', 'CanESM5-r23i1p1f1',
       'CanESM5-r23i1p2f1', 'CanESM5-r24i1p1f1', 'CanESM5-r24i1p2f1',
       'CanESM5-r25i1p1f1', 'CanESM5-r25i1p2f1', 'CanESM5-r2i1p1f1',
       'CanESM5-r2i1p2f1', 'CanESM5-r3i1p1f1', 'CanESM5-r3i1p2f1',
       'CanESM5-r4i1p1f1', 'CanESM5-r4i1p2f1', 'CanESM5-r5i1p1f1',
       'CanESM5-r5i1p2f1', 'CanESM5-r6i1p1f1', 'CanESM5-r6i1p2f1',
       'CanESM5-r7i1p1f1', 'CanESM5-r7i1p2f1', 'CanESM5-r8i1p1f1',
       'CanESM5-r8i1p2f1', 'CanESM5-r9i1p1f1', 'CanESM5-r9i1p2f1',
       'E3SM-1-1-r1i1p1f1', 'EC-Earth3-Veg-r1i1p1f1',
       'EC-Earth3-Veg-r2i1p1f1', 'EC-Earth3-Veg-r3i1p1f1',
       'EC-Earth3-Veg-r4i1p1f1', 'EC-Earth3-Veg-r6i1p1f1',
       'EC-Earth3-r11i1p1f1', 'EC-Earth3-r13i1p1f1',
       'EC-Earth3-r15i1p1f1', 'EC-Earth3-r1i1p1f1', 'EC-Earth3-r3i1p1f1',
       'EC-Earth3-r4i1p1f1', 'EC-Earth3-r6i1p1f1', 'EC-Earth3-r9i1p1f1',
       'FGOALS-f3-L-r1i1p1f1', 'FGOALS-g3-r1i1p1f1', 'FGOALS-g3-r2i1p1f1',
       'FGOALS-g3-r3i1p1f1', 'FGOALS-g3-r4i1p1f1', 'FIO-ESM-2-0-r1i1p1f1',
       'FIO-ESM-2-0-r2i1p1f1', 'FIO-ESM-2-0-r3i1p1f1',
       'GFDL-CM4-r1i1p1f1', 'GFDL-ESM4-r1i1p1f1', 'GISS-E2-1-G-r1i1p3f1',
       'GISS-E2-1-G-r1i1p5f1', 'GISS-E2-1-G-r2i1p3f1',
       'GISS-E2-1-G-r3i1p3f1', 'GISS-E2-1-G-r4i1p3f1',
       'GISS-E2-1-G-r5i1p3f1', 'HadGEM3-GC31-LL-r1i1p1f3',
       'HadGEM3-GC31-LL-r2i1p1f3', 'HadGEM3-GC31-LL-r3i1p1f3',
       'HadGEM3-GC31-LL-r4i1p1f3', 'HadGEM3-GC31-MM-r1i1p1f3',
       'HadGEM3-GC31-MM-r2i1p1f3', 'HadGEM3-GC31-MM-r3i1p1f3',
       'HadGEM3-GC31-MM-r4i1p1f3', 'INM-CM4-8-r1i1p1f1',
       'INM-CM5-0-r1i1p1f1', 'IPSL-CM6A-LR-r14i1p1f1',
       'IPSL-CM6A-LR-r1i1p1f1', 'IPSL-CM6A-LR-r2i1p1f1',
       'IPSL-CM6A-LR-r3i1p1f1', 'IPSL-CM6A-LR-r4i1p1f1',
       'IPSL-CM6A-LR-r6i1p1f1', 'KACE-1-0-G-r1i1p1f1',
       'KACE-1-0-G-r2i1p1f1', 'KACE-1-0-G-r3i1p1f1', 'KIOST-ESM-r1i1p1f1',
       'MIROC-ES2L-r10i1p1f2', 'MIROC-ES2L-r1i1p1f2',
       'MIROC-ES2L-r2i1p1f2', 'MIROC-ES2L-r3i1p1f2',
       'MIROC-ES2L-r4i1p1f2', 'MIROC-ES2L-r5i1p1f2',
       'MIROC-ES2L-r6i1p1f2', 'MIROC-ES2L-r7i1p1f2',
       'MIROC-ES2L-r8i1p1f2', 'MIROC-ES2L-r9i1p1f2', 'MIROC6-r10i1p1f1',
       'MIROC6-r11i1p1f1', 'MIROC6-r12i1p1f1', 'MIROC6-r13i1p1f1',
       'MIROC6-r14i1p1f1', 'MIROC6-r15i1p1f1', 'MIROC6-r16i1p1f1',
       'MIROC6-r17i1p1f1', 'MIROC6-r18i1p1f1', 'MIROC6-r19i1p1f1',
       'MIROC6-r1i1p1f1', 'MIROC6-r20i1p1f1', 'MIROC6-r21i1p1f1',
       'MIROC6-r22i1p1f1', 'MIROC6-r23i1p1f1', 'MIROC6-r24i1p1f1',
       'MIROC6-r25i1p1f1', 'MIROC6-r26i1p1f1', 'MIROC6-r27i1p1f1',
       'MIROC6-r28i1p1f1', 'MIROC6-r29i1p1f1', 'MIROC6-r2i1p1f1',
       'MIROC6-r30i1p1f1', 'MIROC6-r31i1p1f1', 'MIROC6-r32i1p1f1',
       'MIROC6-r33i1p1f1', 'MIROC6-r34i1p1f1', 'MIROC6-r35i1p1f1',
       'MIROC6-r36i1p1f1', 'MIROC6-r37i1p1f1', 'MIROC6-r38i1p1f1',
       'MIROC6-r39i1p1f1', 'MIROC6-r3i1p1f1', 'MIROC6-r40i1p1f1',
       'MIROC6-r41i1p1f1', 'MIROC6-r42i1p1f1', 'MIROC6-r43i1p1f1',
       'MIROC6-r44i1p1f1', 'MIROC6-r45i1p1f1', 'MIROC6-r46i1p1f1',
       'MIROC6-r47i1p1f1', 'MIROC6-r48i1p1f1', 'MIROC6-r49i1p1f1',
       'MIROC6-r4i1p1f1', 'MIROC6-r50i1p1f1', 'MIROC6-r5i1p1f1',
       'MIROC6-r6i1p1f1', 'MIROC6-r7i1p1f1', 'MIROC6-r8i1p1f1',
       'MIROC6-r9i1p1f1', 'MPI-ESM1-2-HR-r1i1p1f1',
       'MPI-ESM1-2-HR-r2i1p1f1', 'MPI-ESM1-2-LR-r10i1p1f1',
       'MPI-ESM1-2-LR-r1i1p1f1', 'MPI-ESM1-2-LR-r2i1p1f1',
       'MPI-ESM1-2-LR-r3i1p1f1', 'MPI-ESM1-2-LR-r4i1p1f1',
       'MPI-ESM1-2-LR-r5i1p1f1', 'MPI-ESM1-2-LR-r6i1p1f1',
       'MPI-ESM1-2-LR-r7i1p1f1', 'MPI-ESM1-2-LR-r8i1p1f1',
       'MPI-ESM1-2-LR-r9i1p1f1', 'MRI-ESM2-0-r1i1p1f1',
       'MRI-ESM2-0-r1i2p1f1', 'NESM3-r1i1p1f1', 'NESM3-r2i1p1f1',
       'NorESM2-LM-r1i1p1f1', 'NorESM2-MM-r1i1p1f1', 'TaiESM1-r1i1p1f1',
       'UKESM1-0-LL-r1i1p1f2', 'UKESM1-0-LL-r2i1p1f2',
       'UKESM1-0-LL-r3i1p1f2', 'UKESM1-0-LL-r4i1p1f2',
       'UKESM1-0-LL-r8i1p1f2']

CMIP6_tas_members = ['ACCESS-CM2-r1i1p1f1', 'ACCESS-CM2-r2i1p1f1',
       'ACCESS-CM2-r3i1p1f1', 'ACCESS-ESM1-5-r10i1p1f1',
       'ACCESS-ESM1-5-r1i1p1f1', 'ACCESS-ESM1-5-r2i1p1f1',
       'ACCESS-ESM1-5-r3i1p1f1', 'ACCESS-ESM1-5-r4i1p1f1',
       'ACCESS-ESM1-5-r5i1p1f1', 'ACCESS-ESM1-5-r6i1p1f1',
       'ACCESS-ESM1-5-r7i1p1f1', 'ACCESS-ESM1-5-r8i1p1f1',
       'ACCESS-ESM1-5-r9i1p1f1', 'AWI-CM-1-1-MR-r1i1p1f1',
       'CAS-ESM2-0-r1i1p1f1', 'CAS-ESM2-0-r3i1p1f1',
       'CESM2-WACCM-r1i1p1f1', 'CESM2-WACCM-r2i1p1f1',
       'CESM2-WACCM-r3i1p1f1', 'CESM2-r10i1p1f1', 'CESM2-r11i1p1f1',
       'CESM2-r1i1p1f1', 'CESM2-r2i1p1f1', 'CESM2-r4i1p1f1',
       'CMCC-CM2-SR5-r1i1p1f1', 'CMCC-ESM2-r1i1p1f1',
       'CNRM-CM6-1-HR-r1i1p1f2', 'CNRM-CM6-1-r1i1p1f2',
       'CNRM-CM6-1-r2i1p1f2', 'CNRM-CM6-1-r3i1p1f2',
       'CNRM-CM6-1-r4i1p1f2', 'CNRM-CM6-1-r5i1p1f2',
       'CNRM-CM6-1-r6i1p1f2', 'CNRM-ESM2-1-r1i1p1f2',
       'CNRM-ESM2-1-r2i1p1f2', 'CNRM-ESM2-1-r3i1p1f2',
       'CNRM-ESM2-1-r4i1p1f2', 'CNRM-ESM2-1-r5i1p1f2',
       'CanESM5-r10i1p1f1', 'CanESM5-r10i1p2f1', 'CanESM5-r11i1p1f1',
       'CanESM5-r11i1p2f1', 'CanESM5-r12i1p1f1', 'CanESM5-r12i1p2f1',
       'CanESM5-r13i1p1f1', 'CanESM5-r13i1p2f1', 'CanESM5-r14i1p1f1',
       'CanESM5-r14i1p2f1', 'CanESM5-r15i1p1f1', 'CanESM5-r15i1p2f1',
       'CanESM5-r16i1p1f1', 'CanESM5-r16i1p2f1', 'CanESM5-r17i1p1f1',
       'CanESM5-r17i1p2f1', 'CanESM5-r18i1p1f1', 'CanESM5-r18i1p2f1',
       'CanESM5-r19i1p1f1', 'CanESM5-r19i1p2f1', 'CanESM5-r1i1p1f1',
       'CanESM5-r1i1p2f1', 'CanESM5-r20i1p1f1', 'CanESM5-r20i1p2f1',
       'CanESM5-r21i1p1f1', 'CanESM5-r21i1p2f1', 'CanESM5-r22i1p1f1',
       'CanESM5-r22i1p2f1', 'CanESM5-r23i1p1f1', 'CanESM5-r23i1p2f1',
       'CanESM5-r24i1p1f1', 'CanESM5-r24i1p2f1', 'CanESM5-r25i1p1f1',
       'CanESM5-r25i1p2f1', 'CanESM5-r2i1p1f1', 'CanESM5-r2i1p2f1',
       'CanESM5-r3i1p1f1', 'CanESM5-r3i1p2f1', 'CanESM5-r4i1p1f1',
       'CanESM5-r4i1p2f1', 'CanESM5-r5i1p1f1', 'CanESM5-r5i1p2f1',
       'CanESM5-r6i1p1f1', 'CanESM5-r6i1p2f1', 'CanESM5-r7i1p1f1',
       'CanESM5-r7i1p2f1', 'CanESM5-r8i1p1f1', 'CanESM5-r8i1p2f1',
       'CanESM5-r9i1p1f1', 'CanESM5-r9i1p2f1', 'E3SM-1-1-r1i1p1f1',
       'EC-Earth3-Veg-r1i1p1f1', 'EC-Earth3-Veg-r2i1p1f1',
       'EC-Earth3-Veg-r3i1p1f1', 'EC-Earth3-Veg-r4i1p1f1',
       'EC-Earth3-r11i1p1f1', 'EC-Earth3-r13i1p1f1',
       'EC-Earth3-r15i1p1f1', 'EC-Earth3-r1i1p1f1', 'EC-Earth3-r3i1p1f1',
       'EC-Earth3-r4i1p1f1', 'EC-Earth3-r6i1p1f1', 'EC-Earth3-r9i1p1f1',
       'FGOALS-f3-L-r1i1p1f1', 'FGOALS-g3-r1i1p1f1', 'FGOALS-g3-r2i1p1f1',
       'FGOALS-g3-r3i1p1f1', 'FGOALS-g3-r4i1p1f1', 'FIO-ESM-2-0-r1i1p1f1',
       'FIO-ESM-2-0-r2i1p1f1', 'FIO-ESM-2-0-r3i1p1f1',
       'GFDL-CM4-r1i1p1f1', 'GFDL-ESM4-r1i1p1f1', 'GISS-E2-1-G-r1i1p3f1',
       'GISS-E2-1-G-r1i1p5f1', 'GISS-E2-1-G-r2i1p3f1',
       'GISS-E2-1-G-r3i1p3f1', 'GISS-E2-1-G-r4i1p3f1',
       'GISS-E2-1-G-r5i1p3f1', 'HadGEM3-GC31-LL-r1i1p1f3',
       'HadGEM3-GC31-LL-r2i1p1f3', 'HadGEM3-GC31-LL-r3i1p1f3',
       'HadGEM3-GC31-LL-r4i1p1f3', 'HadGEM3-GC31-MM-r1i1p1f3',
       'HadGEM3-GC31-MM-r2i1p1f3', 'HadGEM3-GC31-MM-r3i1p1f3',
       'HadGEM3-GC31-MM-r4i1p1f3', 'INM-CM4-8-r1i1p1f1',
       'INM-CM5-0-r1i1p1f1', 'IPSL-CM6A-LR-r14i1p1f1',
       'IPSL-CM6A-LR-r1i1p1f1', 'IPSL-CM6A-LR-r2i1p1f1',
       'IPSL-CM6A-LR-r3i1p1f1', 'IPSL-CM6A-LR-r4i1p1f1',
       'IPSL-CM6A-LR-r6i1p1f1', 'KACE-1-0-G-r1i1p1f1',
       'KACE-1-0-G-r2i1p1f1', 'KACE-1-0-G-r3i1p1f1', 'KIOST-ESM-r1i1p1f1',
       'MCM-UA-1-0-r1i1p1f2', 'MIROC-ES2L-r10i1p1f2',
       'MIROC-ES2L-r1i1p1f2', 'MIROC-ES2L-r2i1p1f2',
       'MIROC-ES2L-r3i1p1f2', 'MIROC-ES2L-r4i1p1f2',
       'MIROC-ES2L-r5i1p1f2', 'MIROC-ES2L-r6i1p1f2',
       'MIROC-ES2L-r7i1p1f2', 'MIROC-ES2L-r8i1p1f2',
       'MIROC-ES2L-r9i1p1f2', 'MIROC6-r10i1p1f1', 'MIROC6-r11i1p1f1',
       'MIROC6-r12i1p1f1', 'MIROC6-r13i1p1f1', 'MIROC6-r14i1p1f1',
       'MIROC6-r15i1p1f1', 'MIROC6-r16i1p1f1', 'MIROC6-r17i1p1f1',
       'MIROC6-r18i1p1f1', 'MIROC6-r19i1p1f1', 'MIROC6-r1i1p1f1',
       'MIROC6-r20i1p1f1', 'MIROC6-r21i1p1f1', 'MIROC6-r22i1p1f1',
       'MIROC6-r23i1p1f1', 'MIROC6-r24i1p1f1', 'MIROC6-r25i1p1f1',
       'MIROC6-r26i1p1f1', 'MIROC6-r27i1p1f1', 'MIROC6-r28i1p1f1',
       'MIROC6-r29i1p1f1', 'MIROC6-r2i1p1f1', 'MIROC6-r30i1p1f1',
       'MIROC6-r31i1p1f1', 'MIROC6-r32i1p1f1', 'MIROC6-r33i1p1f1',
       'MIROC6-r34i1p1f1', 'MIROC6-r35i1p1f1', 'MIROC6-r36i1p1f1',
       'MIROC6-r37i1p1f1', 'MIROC6-r38i1p1f1', 'MIROC6-r39i1p1f1',
       'MIROC6-r3i1p1f1', 'MIROC6-r40i1p1f1', 'MIROC6-r41i1p1f1',
       'MIROC6-r42i1p1f1', 'MIROC6-r43i1p1f1', 'MIROC6-r44i1p1f1',
       'MIROC6-r45i1p1f1', 'MIROC6-r46i1p1f1', 'MIROC6-r47i1p1f1',
       'MIROC6-r48i1p1f1', 'MIROC6-r49i1p1f1', 'MIROC6-r4i1p1f1',
       'MIROC6-r50i1p1f1', 'MIROC6-r5i1p1f1', 'MIROC6-r6i1p1f1',
       'MIROC6-r7i1p1f1', 'MIROC6-r8i1p1f1', 'MIROC6-r9i1p1f1',
       'MPI-ESM1-2-HR-r1i1p1f1', 'MPI-ESM1-2-HR-r2i1p1f1',
       'MPI-ESM1-2-LR-r10i1p1f1', 'MPI-ESM1-2-LR-r1i1p1f1',
       'MPI-ESM1-2-LR-r2i1p1f1', 'MPI-ESM1-2-LR-r3i1p1f1',
       'MPI-ESM1-2-LR-r4i1p1f1', 'MPI-ESM1-2-LR-r5i1p1f1',
       'MPI-ESM1-2-LR-r6i1p1f1', 'MPI-ESM1-2-LR-r7i1p1f1',
       'MPI-ESM1-2-LR-r8i1p1f1', 'MPI-ESM1-2-LR-r9i1p1f1',
       'MRI-ESM2-0-r1i1p1f1', 'MRI-ESM2-0-r1i2p1f1', 'NESM3-r1i1p1f1',
       'NESM3-r2i1p1f1', 'NorESM2-LM-r1i1p1f1', 'NorESM2-MM-r1i1p1f1',
       'TaiESM1-r1i1p1f1', 'UKESM1-0-LL-r1i1p1f2', 'UKESM1-0-LL-r2i1p1f2',
       'UKESM1-0-LL-r3i1p1f2', 'UKESM1-0-LL-r4i1p1f2',
       'UKESM1-0-LL-r8i1p1f2']

CMIP6_psl_members = ['ACCESS-CM2-r1i1p1f1', 'ACCESS-CM2-r2i1p1f1',
       'ACCESS-CM2-r3i1p1f1', 'ACCESS-ESM1-5-r10i1p1f1',
       'ACCESS-ESM1-5-r1i1p1f1', 'ACCESS-ESM1-5-r2i1p1f1',
       'ACCESS-ESM1-5-r3i1p1f1', 'ACCESS-ESM1-5-r4i1p1f1',
       'ACCESS-ESM1-5-r5i1p1f1', 'ACCESS-ESM1-5-r6i1p1f1',
       'ACCESS-ESM1-5-r7i1p1f1', 'ACCESS-ESM1-5-r8i1p1f1',
       'ACCESS-ESM1-5-r9i1p1f1', 'AWI-CM-1-1-MR-r1i1p1f1',
       'BCC-CSM2-MR-r1i1p1f1', 'CAS-ESM2-0-r1i1p1f1',
       'CAS-ESM2-0-r3i1p1f1', 'CESM2-WACCM-r1i1p1f1',
       'CESM2-WACCM-r2i1p1f1', 'CESM2-WACCM-r3i1p1f1', 'CESM2-r10i1p1f1',
       'CESM2-r11i1p1f1', 'CESM2-r1i1p1f1', 'CESM2-r2i1p1f1',
       'CESM2-r4i1p1f1', 'CIESM-r1i1p1f1', 'CMCC-CM2-SR5-r1i1p1f1',
       'CMCC-ESM2-r1i1p1f1', 'CNRM-CM6-1-HR-r1i1p1f2',
       'CNRM-CM6-1-r1i1p1f2', 'CNRM-CM6-1-r2i1p1f2',
       'CNRM-CM6-1-r3i1p1f2', 'CNRM-CM6-1-r4i1p1f2',
       'CNRM-CM6-1-r5i1p1f2', 'CNRM-CM6-1-r6i1p1f2',
       'CNRM-ESM2-1-r1i1p1f2', 'CNRM-ESM2-1-r2i1p1f2',
       'CNRM-ESM2-1-r3i1p1f2', 'CNRM-ESM2-1-r4i1p1f2',
       'CNRM-ESM2-1-r5i1p1f2', 'CanESM5-r10i1p1f1', 'CanESM5-r10i1p2f1',
       'CanESM5-r11i1p1f1', 'CanESM5-r11i1p2f1', 'CanESM5-r12i1p1f1',
       'CanESM5-r12i1p2f1', 'CanESM5-r13i1p1f1', 'CanESM5-r13i1p2f1',
       'CanESM5-r14i1p1f1', 'CanESM5-r14i1p2f1', 'CanESM5-r15i1p1f1',
       'CanESM5-r15i1p2f1', 'CanESM5-r16i1p1f1', 'CanESM5-r16i1p2f1',
       'CanESM5-r17i1p1f1', 'CanESM5-r17i1p2f1', 'CanESM5-r18i1p1f1',
       'CanESM5-r18i1p2f1', 'CanESM5-r19i1p1f1', 'CanESM5-r19i1p2f1',
       'CanESM5-r1i1p1f1', 'CanESM5-r1i1p2f1', 'CanESM5-r20i1p1f1',
       'CanESM5-r20i1p2f1', 'CanESM5-r21i1p1f1', 'CanESM5-r21i1p2f1',
       'CanESM5-r22i1p1f1', 'CanESM5-r22i1p2f1', 'CanESM5-r23i1p1f1',
       'CanESM5-r23i1p2f1', 'CanESM5-r24i1p1f1', 'CanESM5-r24i1p2f1',
       'CanESM5-r25i1p1f1', 'CanESM5-r25i1p2f1', 'CanESM5-r2i1p1f1',
       'CanESM5-r2i1p2f1', 'CanESM5-r3i1p1f1', 'CanESM5-r3i1p2f1',
       'CanESM5-r4i1p1f1', 'CanESM5-r4i1p2f1', 'CanESM5-r5i1p1f1',
       'CanESM5-r5i1p2f1', 'CanESM5-r6i1p1f1', 'CanESM5-r6i1p2f1',
       'CanESM5-r7i1p1f1', 'CanESM5-r7i1p2f1', 'CanESM5-r8i1p1f1',
       'CanESM5-r8i1p2f1', 'CanESM5-r9i1p1f1', 'CanESM5-r9i1p2f1',
       'E3SM-1-1-r1i1p1f1', 'EC-Earth3-Veg-r1i1p1f1',
       'EC-Earth3-Veg-r2i1p1f1', 'EC-Earth3-Veg-r3i1p1f1',
       'EC-Earth3-Veg-r4i1p1f1', 'EC-Earth3-Veg-r6i1p1f1',
       'EC-Earth3-r11i1p1f1', 'EC-Earth3-r13i1p1f1',
       'EC-Earth3-r15i1p1f1', 'EC-Earth3-r1i1p1f1', 'EC-Earth3-r3i1p1f1',
       'EC-Earth3-r4i1p1f1', 'EC-Earth3-r6i1p1f1', 'EC-Earth3-r9i1p1f1',
       'FGOALS-f3-L-r1i1p1f1', 'FGOALS-g3-r1i1p1f1', 'FGOALS-g3-r2i1p1f1',
       'FGOALS-g3-r3i1p1f1', 'FGOALS-g3-r4i1p1f1', 'FIO-ESM-2-0-r1i1p1f1',
       'FIO-ESM-2-0-r2i1p1f1', 'FIO-ESM-2-0-r3i1p1f1',
       'GFDL-CM4-r1i1p1f1', 'GFDL-ESM4-r1i1p1f1', 'GISS-E2-1-G-r1i1p3f1',
       'GISS-E2-1-G-r1i1p5f1', 'GISS-E2-1-G-r2i1p3f1',
       'GISS-E2-1-G-r3i1p3f1', 'GISS-E2-1-G-r4i1p3f1',
       'GISS-E2-1-G-r5i1p3f1', 'HadGEM3-GC31-LL-r1i1p1f3',
       'HadGEM3-GC31-LL-r2i1p1f3', 'HadGEM3-GC31-LL-r3i1p1f3',
       'HadGEM3-GC31-LL-r4i1p1f3', 'HadGEM3-GC31-MM-r1i1p1f3',
       'HadGEM3-GC31-MM-r2i1p1f3', 'HadGEM3-GC31-MM-r3i1p1f3',
       'HadGEM3-GC31-MM-r4i1p1f3', 'INM-CM4-8-r1i1p1f1',
       'INM-CM5-0-r1i1p1f1', 'IPSL-CM6A-LR-r14i1p1f1',
       'IPSL-CM6A-LR-r1i1p1f1', 'IPSL-CM6A-LR-r2i1p1f1',
       'IPSL-CM6A-LR-r3i1p1f1', 'IPSL-CM6A-LR-r4i1p1f1',
       'IPSL-CM6A-LR-r6i1p1f1', 'KACE-1-0-G-r1i1p1f1',
       'KACE-1-0-G-r2i1p1f1', 'KACE-1-0-G-r3i1p1f1', 'KIOST-ESM-r1i1p1f1',
       'MCM-UA-1-0-r1i1p1f2', 'MIROC-ES2L-r10i1p1f2',
       'MIROC-ES2L-r1i1p1f2', 'MIROC-ES2L-r2i1p1f2',
       'MIROC-ES2L-r3i1p1f2', 'MIROC-ES2L-r4i1p1f2',
       'MIROC-ES2L-r5i1p1f2', 'MIROC-ES2L-r6i1p1f2',
       'MIROC-ES2L-r7i1p1f2', 'MIROC-ES2L-r8i1p1f2',
       'MIROC-ES2L-r9i1p1f2', 'MIROC6-r10i1p1f1', 'MIROC6-r11i1p1f1',
       'MIROC6-r12i1p1f1', 'MIROC6-r13i1p1f1', 'MIROC6-r14i1p1f1',
       'MIROC6-r15i1p1f1', 'MIROC6-r16i1p1f1', 'MIROC6-r17i1p1f1',
       'MIROC6-r18i1p1f1', 'MIROC6-r19i1p1f1', 'MIROC6-r1i1p1f1',
       'MIROC6-r20i1p1f1', 'MIROC6-r21i1p1f1', 'MIROC6-r22i1p1f1',
       'MIROC6-r23i1p1f1', 'MIROC6-r24i1p1f1', 'MIROC6-r25i1p1f1',
       'MIROC6-r26i1p1f1', 'MIROC6-r27i1p1f1', 'MIROC6-r28i1p1f1',
       'MIROC6-r29i1p1f1', 'MIROC6-r2i1p1f1', 'MIROC6-r30i1p1f1',
       'MIROC6-r31i1p1f1', 'MIROC6-r32i1p1f1', 'MIROC6-r33i1p1f1',
       'MIROC6-r34i1p1f1', 'MIROC6-r35i1p1f1', 'MIROC6-r36i1p1f1',
       'MIROC6-r37i1p1f1', 'MIROC6-r38i1p1f1', 'MIROC6-r39i1p1f1',
       'MIROC6-r3i1p1f1', 'MIROC6-r40i1p1f1', 'MIROC6-r41i1p1f1',
       'MIROC6-r42i1p1f1', 'MIROC6-r43i1p1f1', 'MIROC6-r44i1p1f1',
       'MIROC6-r45i1p1f1', 'MIROC6-r46i1p1f1', 'MIROC6-r47i1p1f1',
       'MIROC6-r48i1p1f1', 'MIROC6-r49i1p1f1', 'MIROC6-r4i1p1f1',
       'MIROC6-r50i1p1f1', 'MIROC6-r5i1p1f1', 'MIROC6-r6i1p1f1',
       'MIROC6-r7i1p1f1', 'MIROC6-r8i1p1f1', 'MIROC6-r9i1p1f1',
       'MPI-ESM1-2-HR-r1i1p1f1', 'MPI-ESM1-2-HR-r2i1p1f1',
       'MPI-ESM1-2-LR-r10i1p1f1', 'MPI-ESM1-2-LR-r1i1p1f1',
       'MPI-ESM1-2-LR-r2i1p1f1', 'MPI-ESM1-2-LR-r3i1p1f1',
       'MPI-ESM1-2-LR-r4i1p1f1', 'MPI-ESM1-2-LR-r5i1p1f1',
       'MPI-ESM1-2-LR-r6i1p1f1', 'MPI-ESM1-2-LR-r7i1p1f1',
       'MPI-ESM1-2-LR-r8i1p1f1', 'MPI-ESM1-2-LR-r9i1p1f1',
       'MRI-ESM2-0-r1i1p1f1', 'MRI-ESM2-0-r1i2p1f1', 'NESM3-r1i1p1f1',
       'NESM3-r2i1p1f1', 'NorESM2-MM-r1i1p1f1', 'TaiESM1-r1i1p1f1',
       'UKESM1-0-LL-r1i1p1f2', 'UKESM1-0-LL-r2i1p1f2',
       'UKESM1-0-LL-r3i1p1f2', 'UKESM1-0-LL-r4i1p1f2',
       'UKESM1-0-LL-r8i1p1f2']

CMIP6_ECS_members = ['ACCESS-CM2-r1i1p1f1', 'ACCESS-CM2-r2i1p1f1', 'ACCESS-CM2-r3i1p1f1',
       'ACCESS-ESM1-5-r10i1p1f1', 'ACCESS-ESM1-5-r1i1p1f1',
       'ACCESS-ESM1-5-r2i1p1f1', 'ACCESS-ESM1-5-r3i1p1f1',
       'ACCESS-ESM1-5-r4i1p1f1', 'ACCESS-ESM1-5-r5i1p1f1',
       'ACCESS-ESM1-5-r6i1p1f1', 'ACCESS-ESM1-5-r7i1p1f1',
       'ACCESS-ESM1-5-r8i1p1f1', 'ACCESS-ESM1-5-r9i1p1f1',
       'AWI-CM-1-1-MR-r1i1p1f1', 'CAS-ESM2-0-r1i1p1f1', 'CAS-ESM2-0-r3i1p1f1',
       'CESM2-WACCM-r1i1p1f1', 'CESM2-WACCM-r2i1p1f1', 'CESM2-WACCM-r3i1p1f1',
       'CESM2-r10i1p1f1', 'CESM2-r11i1p1f1', 'CESM2-r1i1p1f1',
       'CESM2-r2i1p1f1', 'CESM2-r4i1p1f1', 'CMCC-CM2-SR5-r1i1p1f1',
       'CMCC-ESM2-r1i1p1f1', 'CNRM-CM6-1-HR-r1i1p1f2', 'CNRM-CM6-1-r1i1p1f2',
       'CNRM-CM6-1-r2i1p1f2', 'CNRM-CM6-1-r3i1p1f2', 'CNRM-CM6-1-r4i1p1f2',
       'CNRM-CM6-1-r5i1p1f2', 'CNRM-CM6-1-r6i1p1f2', 'CNRM-ESM2-1-r1i1p1f2',
       'CNRM-ESM2-1-r2i1p1f2', 'CNRM-ESM2-1-r3i1p1f2', 'CNRM-ESM2-1-r4i1p1f2',
       'CNRM-ESM2-1-r5i1p1f2', 'CanESM5-r10i1p1f1', 'CanESM5-r10i1p2f1',
       'CanESM5-r11i1p1f1', 'CanESM5-r11i1p2f1', 'CanESM5-r12i1p1f1',
       'CanESM5-r12i1p2f1', 'CanESM5-r13i1p1f1', 'CanESM5-r13i1p2f1',
       'CanESM5-r14i1p1f1', 'CanESM5-r14i1p2f1', 'CanESM5-r15i1p1f1',
       'CanESM5-r15i1p2f1', 'CanESM5-r16i1p1f1', 'CanESM5-r16i1p2f1',
       'CanESM5-r17i1p1f1', 'CanESM5-r17i1p2f1', 'CanESM5-r18i1p1f1',
       'CanESM5-r18i1p2f1', 'CanESM5-r19i1p1f1', 'CanESM5-r19i1p2f1',
       'CanESM5-r1i1p1f1', 'CanESM5-r1i1p2f1', 'CanESM5-r20i1p1f1',
       'CanESM5-r20i1p2f1', 'CanESM5-r21i1p1f1', 'CanESM5-r21i1p2f1',
       'CanESM5-r22i1p1f1', 'CanESM5-r22i1p2f1', 'CanESM5-r23i1p1f1',
       'CanESM5-r23i1p2f1', 'CanESM5-r24i1p1f1', 'CanESM5-r24i1p2f1',
       'CanESM5-r25i1p1f1', 'CanESM5-r25i1p2f1', 'CanESM5-r2i1p1f1',
       'CanESM5-r2i1p2f1', 'CanESM5-r3i1p1f1', 'CanESM5-r3i1p2f1',
       'CanESM5-r4i1p1f1', 'CanESM5-r4i1p2f1', 'CanESM5-r5i1p1f1',
       'CanESM5-r5i1p2f1', 'CanESM5-r6i1p1f1', 'CanESM5-r6i1p2f1',
       'CanESM5-r7i1p1f1', 'CanESM5-r7i1p2f1', 'CanESM5-r8i1p1f1',
       'CanESM5-r8i1p2f1', 'CanESM5-r9i1p1f1', 'CanESM5-r9i1p2f1',
       'E3SM-1-1-r1i1p1f1',
       'EC-Earth3-Veg-r1i1p1f1', 'EC-Earth3-Veg-r2i1p1f1',
       'EC-Earth3-Veg-r3i1p1f1', 'EC-Earth3-Veg-r4i1p1f1',
       'EC-Earth3-r11i1p1f1', 'EC-Earth3-r13i1p1f1',
       'EC-Earth3-r15i1p1f1', 'EC-Earth3-r1i1p1f1', 'EC-Earth3-r3i1p1f1',
       'EC-Earth3-r4i1p1f1', 'EC-Earth3-r6i1p1f1', 'EC-Earth3-r9i1p1f1',
       'FGOALS-f3-L-r1i1p1f1', 'FGOALS-g3-r1i1p1f1',
       'FGOALS-g3-r2i1p1f1', 'GFDL-CM4-r1i1p1f1', 'GFDL-ESM4-r1i1p1f1',
       'GISS-E2-1-G-r1i1p3f1', 'HadGEM3-GC31-LL-r1i1p1f3',
       'HadGEM3-GC31-LL-r2i1p1f3', 'HadGEM3-GC31-LL-r3i1p1f3',
       'HadGEM3-GC31-LL-r4i1p1f3', 'HadGEM3-GC31-MM-r1i1p1f3',
       'HadGEM3-GC31-MM-r2i1p1f3', 'HadGEM3-GC31-MM-r3i1p1f3',
       'HadGEM3-GC31-MM-r4i1p1f3', 'INM-CM4-8-r1i1p1f1', 'INM-CM5-0-r1i1p1f1',
       'IPSL-CM6A-LR-r14i1p1f1', 'IPSL-CM6A-LR-r1i1p1f1',
       'IPSL-CM6A-LR-r2i1p1f1', 'IPSL-CM6A-LR-r3i1p1f1',
       'IPSL-CM6A-LR-r4i1p1f1', 'IPSL-CM6A-LR-r6i1p1f1', 'KACE-1-0-G-r2i1p1f1',
       'KACE-1-0-G-r3i1p1f1', 'KIOST-ESM-r1i1p1f1','MCM-UA-1-0-r1i1p1f2','MIROC-ES2L-r10i1p1f2',
       'MIROC-ES2L-r1i1p1f2', 'MIROC-ES2L-r2i1p1f2', 'MIROC-ES2L-r3i1p1f2',
       'MIROC-ES2L-r4i1p1f2', 'MIROC-ES2L-r5i1p1f2', 'MIROC-ES2L-r6i1p1f2',
       'MIROC-ES2L-r7i1p1f2', 'MIROC-ES2L-r8i1p1f2', 'MIROC-ES2L-r9i1p1f2',
       'MIROC6-r10i1p1f1', 'MIROC6-r11i1p1f1', 'MIROC6-r12i1p1f1',
       'MIROC6-r13i1p1f1', 'MIROC6-r14i1p1f1', 'MIROC6-r15i1p1f1',
       'MIROC6-r16i1p1f1', 'MIROC6-r17i1p1f1', 'MIROC6-r18i1p1f1',
       'MIROC6-r19i1p1f1', 'MIROC6-r1i1p1f1', 'MIROC6-r20i1p1f1',
       'MIROC6-r21i1p1f1', 'MIROC6-r22i1p1f1', 'MIROC6-r23i1p1f1',
       'MIROC6-r24i1p1f1', 'MIROC6-r25i1p1f1', 'MIROC6-r26i1p1f1',
       'MIROC6-r27i1p1f1', 'MIROC6-r28i1p1f1', 'MIROC6-r29i1p1f1',
       'MIROC6-r2i1p1f1', 'MIROC6-r30i1p1f1', 'MIROC6-r31i1p1f1',
       'MIROC6-r32i1p1f1', 'MIROC6-r33i1p1f1', 'MIROC6-r34i1p1f1',
       'MIROC6-r35i1p1f1', 'MIROC6-r36i1p1f1', 'MIROC6-r37i1p1f1',
       'MIROC6-r38i1p1f1', 'MIROC6-r39i1p1f1', 'MIROC6-r3i1p1f1',
       'MIROC6-r40i1p1f1', 'MIROC6-r41i1p1f1', 'MIROC6-r42i1p1f1',
       'MIROC6-r43i1p1f1', 'MIROC6-r44i1p1f1', 'MIROC6-r45i1p1f1',
       'MIROC6-r46i1p1f1', 'MIROC6-r47i1p1f1', 'MIROC6-r48i1p1f1',
       'MIROC6-r49i1p1f1', 'MIROC6-r4i1p1f1', 'MIROC6-r50i1p1f1',
       'MIROC6-r5i1p1f1', 'MIROC6-r6i1p1f1', 'MIROC6-r7i1p1f1',
       'MIROC6-r8i1p1f1', 'MIROC6-r9i1p1f1', 'MPI-ESM1-2-HR-r1i1p1f1',
       'MPI-ESM1-2-HR-r2i1p1f1', 'MPI-ESM1-2-LR-r10i1p1f1',
       'MPI-ESM1-2-LR-r1i1p1f1', 'MPI-ESM1-2-LR-r2i1p1f1',
       'MPI-ESM1-2-LR-r3i1p1f1', 'MPI-ESM1-2-LR-r4i1p1f1',
       'MPI-ESM1-2-LR-r5i1p1f1', 'MPI-ESM1-2-LR-r6i1p1f1',
       'MPI-ESM1-2-LR-r7i1p1f1', 'MPI-ESM1-2-LR-r8i1p1f1',
       'MPI-ESM1-2-LR-r9i1p1f1', 'MRI-ESM2-0-r1i1p1f1', 'MRI-ESM2-0-r1i2p1f1',
       'NESM3-r1i1p1f1', 'NESM3-r2i1p1f1', 'NorESM2-MM-r1i1p1f1',
       'TaiESM1-r1i1p1f1', 'UKESM1-0-LL-r1i1p1f2', 'UKESM1-0-LL-r2i1p1f2',
       'UKESM1-0-LL-r3i1p1f2', 'UKESM1-0-LL-r4i1p1f2', 'UKESM1-0-LL-r8i1p1f2']

### select predictors here ###
CMIP6_predictor_choices = (CMIP6_tos_members, CMIP6_swcre_members, CMIP6_pr_members,CMIP6_tas_members,CMIP6_ECS_members)
CMIP6_common_members = reduce(np.intersect1d, CMIP6_predictor_choices)

# members available for each predictor, CMIP5
CMIP5_tos_members = ['ACCESS1-0-r1i1p1', 'ACCESS1-3-r1i1p1', 'BNU-ESM-r1i1p1',
       'CCSM4-r1i1p1', 'CCSM4-r2i1p1', 'CCSM4-r3i1p1', 'CCSM4-r4i1p1',
       'CCSM4-r5i1p1', 'CCSM4-r6i1p1', 'CESM1-BGC-r1i1p1', 'CESM1-CAM5-r1i1p1',
       'CESM1-CAM5-r2i1p1', 'CESM1-CAM5-r3i1p1', 'CMCC-CESM-r1i1p1',
       'CMCC-CM-r1i1p1', 'CMCC-CMS-r1i1p1', 'CNRM-CM5-r10i1p1',
       'CNRM-CM5-r1i1p1', 'CNRM-CM5-r2i1p1', 'CNRM-CM5-r4i1p1',
       'CNRM-CM5-r6i1p1', 'CSIRO-Mk3-6-0-r10i1p1', 'CSIRO-Mk3-6-0-r1i1p1',
       'CSIRO-Mk3-6-0-r2i1p1', 'CSIRO-Mk3-6-0-r3i1p1', 'CSIRO-Mk3-6-0-r4i1p1',
       'CSIRO-Mk3-6-0-r5i1p1', 'CSIRO-Mk3-6-0-r6i1p1', 'CSIRO-Mk3-6-0-r7i1p1',
       'CSIRO-Mk3-6-0-r8i1p1', 'CSIRO-Mk3-6-0-r9i1p1', 'CanESM2-r1i1p1',
       'CanESM2-r2i1p1', 'CanESM2-r3i1p1', 'CanESM2-r4i1p1', 'CanESM2-r5i1p1',
       'EC-EARTH-r10i1p1', 'EC-EARTH-r11i1p1', 'EC-EARTH-r12i1p1',
       'EC-EARTH-r13i1p1', 'EC-EARTH-r14i1p1', 'EC-EARTH-r1i1p1',
       'EC-EARTH-r2i1p1', 'EC-EARTH-r3i1p1', 'EC-EARTH-r6i1p1',
       'EC-EARTH-r7i1p1', 'EC-EARTH-r8i1p1', 'EC-EARTH-r9i1p1',
       'FIO-ESM-r1i1p1', 'FIO-ESM-r2i1p1', 'FIO-ESM-r3i1p1', 'GFDL-CM3-r1i1p1',
       'GFDL-ESM2G-r1i1p1', 'GFDL-ESM2M-r1i1p1', 'GISS-E2-H-CC-r1i1p1',
       'GISS-E2-H-r1i1p1', 'GISS-E2-H-r1i1p2', 'GISS-E2-H-r1i1p3',
       'GISS-E2-H-r2i1p1', 'GISS-E2-H-r2i1p3', 'GISS-E2-R-CC-r1i1p1',
       'GISS-E2-R-r1i1p1', 'GISS-E2-R-r1i1p2', 'GISS-E2-R-r1i1p3',
       'GISS-E2-R-r2i1p1', 'GISS-E2-R-r2i1p3', 'HadGEM2-AO-r1i1p1',
       'HadGEM2-CC-r1i1p1', 'HadGEM2-ES-r1i1p1', 'HadGEM2-ES-r2i1p1',
       'HadGEM2-ES-r3i1p1', 'HadGEM2-ES-r4i1p1', 'IPSL-CM5A-LR-r1i1p1',
       'IPSL-CM5A-LR-r2i1p1', 'IPSL-CM5A-LR-r3i1p1', 'IPSL-CM5A-LR-r4i1p1',
       'IPSL-CM5A-MR-r1i1p1', 'IPSL-CM5B-LR-r1i1p1', 'MIROC-ESM-CHEM-r1i1p1',
       'MIROC-ESM-r1i1p1', 'MIROC5-r1i1p1', 'MIROC5-r2i1p1', 'MIROC5-r3i1p1',
       'MPI-ESM-LR-r1i1p1', 'MPI-ESM-LR-r2i1p1', 'MPI-ESM-LR-r3i1p1',
       'MPI-ESM-MR-r1i1p1', 'MRI-CGCM3-r1i1p1', 'MRI-ESM1-r1i1p1',
       'NorESM1-M-r1i1p1', 'NorESM1-ME-r1i1p1', 'bcc-csm1-1-m-r1i1p1',
       'bcc-csm1-1-r1i1p1', 'inmcm4-r1i1p1']

CMIP5_swcre_members = ['ACCESS1-0-r1i1p1', 'ACCESS1-3-r1i1p1', 'CCSM4-r1i1p1', 'CCSM4-r2i1p1',
       'CCSM4-r3i1p1', 'CCSM4-r4i1p1', 'CCSM4-r5i1p1', 'CCSM4-r6i1p1',
       'CESM1-BGC-r1i1p1', 'CESM1-CAM5-r1i1p1', 'CESM1-CAM5-r2i1p1',
       'CESM1-CAM5-r3i1p1', 'CNRM-CM5-r10i1p1', 'CNRM-CM5-r1i1p1',
       'CNRM-CM5-r2i1p1', 'CNRM-CM5-r4i1p1', 'CNRM-CM5-r6i1p1',
       'CSIRO-Mk3-6-0-r10i1p1', 'CSIRO-Mk3-6-0-r1i1p1', 'CSIRO-Mk3-6-0-r2i1p1',
       'CSIRO-Mk3-6-0-r3i1p1', 'CSIRO-Mk3-6-0-r4i1p1', 'CSIRO-Mk3-6-0-r5i1p1',
       'CSIRO-Mk3-6-0-r6i1p1', 'CSIRO-Mk3-6-0-r7i1p1', 'CSIRO-Mk3-6-0-r8i1p1',
       'CSIRO-Mk3-6-0-r9i1p1', 'CanESM2-r1i1p1', 'CanESM2-r2i1p1',
       'CanESM2-r3i1p1', 'CanESM2-r4i1p1', 'CanESM2-r5i1p1',
       'FGOALS-g2-r1i1p1', 'FIO-ESM-r1i1p1', 'FIO-ESM-r2i1p1',
       'FIO-ESM-r3i1p1', 'GFDL-CM3-r1i1p1', 'GFDL-ESM2G-r1i1p1',
       'GFDL-ESM2M-r1i1p1', 'GISS-E2-H-CC-r1i1p1', 'GISS-E2-H-r1i1p1',
       'GISS-E2-H-r1i1p2', 'GISS-E2-H-r1i1p3', 'GISS-E2-H-r2i1p1',
       'GISS-E2-H-r2i1p3', 'GISS-E2-R-CC-r1i1p1', 'GISS-E2-R-r1i1p1',
       'GISS-E2-R-r1i1p2', 'GISS-E2-R-r1i1p3', 'GISS-E2-R-r2i1p1',
       'GISS-E2-R-r2i1p3', 'HadGEM2-AO-r1i1p1', 'HadGEM2-CC-r1i1p1',
       'HadGEM2-ES-r1i1p1', 'HadGEM2-ES-r2i1p1', 'HadGEM2-ES-r3i1p1',
       'HadGEM2-ES-r4i1p1', 'IPSL-CM5A-LR-r1i1p1', 'IPSL-CM5A-LR-r2i1p1',
       'IPSL-CM5A-LR-r3i1p1', 'IPSL-CM5A-LR-r4i1p1', 'IPSL-CM5A-MR-r1i1p1',
       'IPSL-CM5B-LR-r1i1p1', 'MIROC-ESM-CHEM-r1i1p1', 'MIROC-ESM-r1i1p1',
       'MIROC5-r1i1p1', 'MIROC5-r2i1p1', 'MIROC5-r3i1p1', 'MPI-ESM-LR-r1i1p1',
       'MPI-ESM-LR-r2i1p1', 'MPI-ESM-LR-r3i1p1', 'MPI-ESM-MR-r1i1p1',
       'MRI-CGCM3-r1i1p1', 'MRI-ESM1-r1i1p1', 'NorESM1-M-r1i1p1',
       'NorESM1-ME-r1i1p1', 'bcc-csm1-1-m-r1i1p1', 'bcc-csm1-1-r1i1p1',
       'inmcm4-r1i1p1']

CMIP5_pr_members = ['ACCESS1-0-r1i1p1', 'ACCESS1-3-r1i1p1', 'BNU-ESM-r1i1p1',
       'CCSM4-r1i1p1', 'CCSM4-r2i1p1', 'CCSM4-r3i1p1', 'CCSM4-r4i1p1',
       'CCSM4-r5i1p1', 'CCSM4-r6i1p1', 'CESM1-BGC-r1i1p1', 'CESM1-CAM5-r1i1p1',
       'CESM1-CAM5-r2i1p1', 'CESM1-CAM5-r3i1p1', 'CMCC-CESM-r1i1p1',
       'CMCC-CM-r1i1p1', 'CMCC-CMS-r1i1p1', 'CNRM-CM5-r10i1p1',
       'CNRM-CM5-r1i1p1', 'CNRM-CM5-r2i1p1', 'CNRM-CM5-r4i1p1',
       'CNRM-CM5-r6i1p1', 'CSIRO-Mk3-6-0-r10i1p1', 'CSIRO-Mk3-6-0-r1i1p1',
       'CSIRO-Mk3-6-0-r2i1p1', 'CSIRO-Mk3-6-0-r3i1p1', 'CSIRO-Mk3-6-0-r4i1p1',
       'CSIRO-Mk3-6-0-r5i1p1', 'CSIRO-Mk3-6-0-r6i1p1', 'CSIRO-Mk3-6-0-r7i1p1',
       'CSIRO-Mk3-6-0-r8i1p1', 'CSIRO-Mk3-6-0-r9i1p1', 'CanESM2-r1i1p1',
       'CanESM2-r2i1p1', 'CanESM2-r3i1p1', 'CanESM2-r4i1p1', 'CanESM2-r5i1p1',
       'EC-EARTH-r12i1p1', 'EC-EARTH-r13i1p1', 'EC-EARTH-r1i1p1',
       'EC-EARTH-r2i1p1', 'EC-EARTH-r8i1p1', 'EC-EARTH-r9i1p1',
       'FGOALS-g2-r1i1p1', 'FIO-ESM-r1i1p1', 'FIO-ESM-r2i1p1',
       'FIO-ESM-r3i1p1', 'GFDL-CM3-r1i1p1', 'GFDL-ESM2G-r1i1p1',
       'GFDL-ESM2M-r1i1p1', 'GISS-E2-H-CC-r1i1p1', 'GISS-E2-H-r1i1p1',
       'GISS-E2-H-r1i1p2', 'GISS-E2-H-r1i1p3', 'GISS-E2-H-r2i1p1',
       'GISS-E2-H-r2i1p3', 'GISS-E2-R-CC-r1i1p1', 'GISS-E2-R-r1i1p1',
       'GISS-E2-R-r1i1p2', 'GISS-E2-R-r1i1p3', 'GISS-E2-R-r2i1p1',
       'GISS-E2-R-r2i1p3', 'HadGEM2-AO-r1i1p1', 'HadGEM2-CC-r1i1p1',
       'HadGEM2-ES-r1i1p1', 'HadGEM2-ES-r2i1p1', 'HadGEM2-ES-r3i1p1',
       'HadGEM2-ES-r4i1p1', 'IPSL-CM5A-LR-r1i1p1', 'IPSL-CM5A-LR-r2i1p1',
       'IPSL-CM5A-LR-r3i1p1', 'IPSL-CM5A-LR-r4i1p1', 'IPSL-CM5A-MR-r1i1p1',
       'IPSL-CM5B-LR-r1i1p1', 'MIROC-ESM-CHEM-r1i1p1', 'MIROC-ESM-r1i1p1',
       'MIROC5-r1i1p1', 'MIROC5-r2i1p1', 'MIROC5-r3i1p1', 'MPI-ESM-LR-r1i1p1',
       'MPI-ESM-LR-r2i1p1', 'MPI-ESM-LR-r3i1p1', 'MPI-ESM-MR-r1i1p1',
       'MRI-CGCM3-r1i1p1', 'MRI-ESM1-r1i1p1', 'NorESM1-M-r1i1p1',
       'NorESM1-ME-r1i1p1', 'bcc-csm1-1-m-r1i1p1', 'bcc-csm1-1-r1i1p1',
       'inmcm4-r1i1p1']

CMIP5_tas_members = ['ACCESS1-0-r1i1p1', 'ACCESS1-3-r1i1p1', 'BNU-ESM-r1i1p1',
       'CCSM4-r1i1p1', 'CCSM4-r2i1p1', 'CCSM4-r3i1p1', 'CCSM4-r4i1p1',
       'CCSM4-r5i1p1', 'CCSM4-r6i1p1', 'CESM1-BGC-r1i1p1', 'CESM1-CAM5-r1i1p1',
       'CESM1-CAM5-r2i1p1', 'CESM1-CAM5-r3i1p1', 'CMCC-CESM-r1i1p1',
       'CMCC-CM-r1i1p1', 'CMCC-CMS-r1i1p1', 'CNRM-CM5-r10i1p1',
       'CNRM-CM5-r1i1p1', 'CNRM-CM5-r2i1p1', 'CNRM-CM5-r4i1p1',
       'CNRM-CM5-r6i1p1', 'CSIRO-Mk3-6-0-r10i1p1', 'CSIRO-Mk3-6-0-r1i1p1',
       'CSIRO-Mk3-6-0-r2i1p1', 'CSIRO-Mk3-6-0-r3i1p1', 'CSIRO-Mk3-6-0-r4i1p1',
       'CSIRO-Mk3-6-0-r5i1p1', 'CSIRO-Mk3-6-0-r6i1p1', 'CSIRO-Mk3-6-0-r7i1p1',
       'CSIRO-Mk3-6-0-r8i1p1', 'CSIRO-Mk3-6-0-r9i1p1', 'CanESM2-r1i1p1',
       'CanESM2-r2i1p1', 'CanESM2-r3i1p1', 'CanESM2-r4i1p1', 'CanESM2-r5i1p1',
       'EC-EARTH-r12i1p1', 'EC-EARTH-r13i1p1', 'EC-EARTH-r1i1p1',
       'EC-EARTH-r2i1p1', 'EC-EARTH-r8i1p1', 'EC-EARTH-r9i1p1',
       'FGOALS-g2-r1i1p1', 'FIO-ESM-r1i1p1', 'FIO-ESM-r2i1p1',
       'FIO-ESM-r3i1p1', 'GFDL-CM3-r1i1p1', 'GFDL-ESM2G-r1i1p1',
       'GFDL-ESM2M-r1i1p1', 'GISS-E2-H-CC-r1i1p1', 'GISS-E2-H-r1i1p1',
       'GISS-E2-H-r1i1p2', 'GISS-E2-H-r1i1p3', 'GISS-E2-H-r2i1p1',
       'GISS-E2-H-r2i1p3', 'GISS-E2-R-CC-r1i1p1', 'GISS-E2-R-r1i1p1',
       'GISS-E2-R-r1i1p2', 'GISS-E2-R-r1i1p3', 'GISS-E2-R-r2i1p1',
       'GISS-E2-R-r2i1p3', 'HadGEM2-AO-r1i1p1', 'HadGEM2-CC-r1i1p1',
       'HadGEM2-ES-r1i1p1', 'HadGEM2-ES-r2i1p1', 'HadGEM2-ES-r3i1p1',
       'HadGEM2-ES-r4i1p1', 'IPSL-CM5A-LR-r1i1p1', 'IPSL-CM5A-LR-r2i1p1',
       'IPSL-CM5A-LR-r3i1p1', 'IPSL-CM5A-LR-r4i1p1', 'IPSL-CM5A-MR-r1i1p1',
       'IPSL-CM5B-LR-r1i1p1', 'MIROC-ESM-CHEM-r1i1p1', 'MIROC-ESM-r1i1p1',
       'MIROC5-r1i1p1', 'MIROC5-r2i1p1', 'MIROC5-r3i1p1', 'MPI-ESM-LR-r1i1p1',
       'MPI-ESM-LR-r2i1p1', 'MPI-ESM-LR-r3i1p1', 'MPI-ESM-MR-r1i1p1',
       'MRI-CGCM3-r1i1p1', 'MRI-ESM1-r1i1p1', 'NorESM1-M-r1i1p1',
       'NorESM1-ME-r1i1p1', 'bcc-csm1-1-m-r1i1p1', 'bcc-csm1-1-r1i1p1',
       'inmcm4-r1i1p1']

CMIP5_psl_members = ['ACCESS1-0-r1i1p1', 'ACCESS1-3-r1i1p1', 'BNU-ESM-r1i1p1',
       'CCSM4-r1i1p1', 'CCSM4-r2i1p1', 'CCSM4-r3i1p1', 'CCSM4-r4i1p1',
       'CCSM4-r5i1p1', 'CCSM4-r6i1p1', 'CESM1-BGC-r1i1p1', 'CESM1-CAM5-r1i1p1',
       'CESM1-CAM5-r2i1p1', 'CESM1-CAM5-r3i1p1', 'CMCC-CESM-r1i1p1',
       'CMCC-CM-r1i1p1', 'CMCC-CMS-r1i1p1', 'CNRM-CM5-r10i1p1',
       'CNRM-CM5-r1i1p1', 'CNRM-CM5-r2i1p1', 'CNRM-CM5-r4i1p1',
       'CNRM-CM5-r6i1p1', 'CSIRO-Mk3-6-0-r10i1p1', 'CSIRO-Mk3-6-0-r1i1p1',
       'CSIRO-Mk3-6-0-r2i1p1', 'CSIRO-Mk3-6-0-r3i1p1', 'CSIRO-Mk3-6-0-r4i1p1',
       'CSIRO-Mk3-6-0-r5i1p1', 'CSIRO-Mk3-6-0-r6i1p1', 'CSIRO-Mk3-6-0-r7i1p1',
       'CSIRO-Mk3-6-0-r8i1p1', 'CSIRO-Mk3-6-0-r9i1p1', 'CanESM2-r1i1p1',
       'CanESM2-r2i1p1', 'CanESM2-r3i1p1', 'CanESM2-r4i1p1', 'CanESM2-r5i1p1',
       'EC-EARTH-r12i1p1', 'EC-EARTH-r1i1p1', 'EC-EARTH-r2i1p1',
       'EC-EARTH-r8i1p1', 'EC-EARTH-r9i1p1', 'FGOALS-g2-r1i1p1',
       'FIO-ESM-r1i1p1', 'FIO-ESM-r2i1p1', 'FIO-ESM-r3i1p1', 'GFDL-CM3-r1i1p1',
       'GFDL-ESM2G-r1i1p1', 'GFDL-ESM2M-r1i1p1', 'GISS-E2-H-CC-r1i1p1',
       'GISS-E2-H-r1i1p1', 'GISS-E2-H-r1i1p2', 'GISS-E2-H-r1i1p3',
       'GISS-E2-H-r2i1p1', 'GISS-E2-H-r2i1p3', 'GISS-E2-R-CC-r1i1p1',
       'GISS-E2-R-r1i1p1', 'GISS-E2-R-r1i1p2', 'GISS-E2-R-r1i1p3',
       'GISS-E2-R-r2i1p1', 'GISS-E2-R-r2i1p3', 'HadGEM2-AO-r1i1p1',
       'HadGEM2-CC-r1i1p1', 'HadGEM2-ES-r1i1p1', 'HadGEM2-ES-r2i1p1',
       'HadGEM2-ES-r3i1p1', 'HadGEM2-ES-r4i1p1', 'IPSL-CM5A-LR-r1i1p1',
       'IPSL-CM5A-LR-r2i1p1', 'IPSL-CM5A-LR-r3i1p1', 'IPSL-CM5A-LR-r4i1p1',
       'IPSL-CM5A-MR-r1i1p1', 'IPSL-CM5B-LR-r1i1p1', 'MIROC-ESM-CHEM-r1i1p1',
       'MIROC-ESM-r1i1p1', 'MIROC5-r1i1p1', 'MIROC5-r2i1p1', 'MIROC5-r3i1p1',
       'MPI-ESM-LR-r1i1p1', 'MPI-ESM-LR-r2i1p1', 'MPI-ESM-LR-r3i1p1',
       'MPI-ESM-MR-r1i1p1', 'MRI-CGCM3-r1i1p1', 'MRI-ESM1-r1i1p1',
       'NorESM1-M-r1i1p1', 'NorESM1-ME-r1i1p1', 'bcc-csm1-1-m-r1i1p1',
       'bcc-csm1-1-r1i1p1', 'inmcm4-r1i1p1']

CMIP5_ECS_members = ['ACCESS1-0-r1i1p1', 'ACCESS1-3-r1i1p1','BNU-ESM-r1i1p1', 'CCSM4-r1i1p1', 'CCSM4-r2i1p1',
           'CCSM4-r3i1p1', 'CCSM4-r4i1p1', 'CCSM4-r5i1p1', 'CCSM4-r6i1p1',
           'CESM1-CAM5-r1i1p1', 'CESM1-CAM5-r2i1p1', 'CESM1-CAM5-r3i1p1',
           'CNRM-CM5-r10i1p1', 'CNRM-CM5-r1i1p1', 'CNRM-CM5-r2i1p1',
           'CNRM-CM5-r4i1p1', 'CNRM-CM5-r6i1p1', 'CSIRO-Mk3-6-0-r10i1p1',
           'CSIRO-Mk3-6-0-r1i1p1', 'CSIRO-Mk3-6-0-r2i1p1', 'CSIRO-Mk3-6-0-r3i1p1',
           'CSIRO-Mk3-6-0-r4i1p1', 'CSIRO-Mk3-6-0-r5i1p1', 'CSIRO-Mk3-6-0-r6i1p1',
           'CSIRO-Mk3-6-0-r7i1p1', 'CSIRO-Mk3-6-0-r8i1p1', 'CSIRO-Mk3-6-0-r9i1p1',
           'CanESM2-r1i1p1', 'CanESM2-r2i1p1', 'CanESM2-r3i1p1', 'CanESM2-r4i1p1',
           'CanESM2-r5i1p1', 'EC-EARTH-r12i1p1', 'EC-EARTH-r1i1p1', 'EC-EARTH-r2i1p1',
           'EC-EARTH-r8i1p1', 'EC-EARTH-r9i1p1','FGOALS-g2-r1i1p1','GFDL-CM3-r1i1p1', 'GFDL-ESM2G-r1i1p1',
           'GFDL-ESM2M-r1i1p1', 'GISS-E2-H-r1i1p1', 'GISS-E2-H-r1i1p2',
           'GISS-E2-H-r1i1p3', 'GISS-E2-H-r2i1p1', 'GISS-E2-H-r2i1p3',
           'GISS-E2-R-r1i1p1', 'GISS-E2-R-r1i1p2', 'GISS-E2-R-r1i1p3',
           'GISS-E2-R-r2i1p1', 'GISS-E2-R-r2i1p3', 'HadGEM2-ES-r1i1p1',
           'HadGEM2-ES-r2i1p1', 'HadGEM2-ES-r3i1p1', 'HadGEM2-ES-r4i1p1',
           'IPSL-CM5A-LR-r1i1p1', 'IPSL-CM5A-LR-r2i1p1', 'IPSL-CM5A-LR-r3i1p1',
           'IPSL-CM5A-LR-r4i1p1', 'IPSL-CM5A-MR-r1i1p1', 'IPSL-CM5B-LR-r1i1p1',
           'MIROC-ESM-r1i1p1', 'MIROC5-r1i1p1', 'MIROC5-r2i1p1', 'MIROC5-r3i1p1',
           'MPI-ESM-LR-r1i1p1', 'MPI-ESM-LR-r2i1p1', 'MPI-ESM-LR-r3i1p1',
           'MPI-ESM-MR-r1i1p1', 'MRI-CGCM3-r1i1p1', 'NorESM1-M-r1i1p1',
           'NorESM1-ME-r1i1p1', 'bcc-csm1-1-m-r1i1p1', 'bcc-csm1-1-r1i1p1',
           'inmcm4-r1i1p1']

### select predictors here ###
CMIP5_predictor_choices = (CMIP5_tos_members, CMIP5_swcre_members, CMIP5_pr_members,CMIP5_tas_members,CMIP5_ECS_members)
CMIP5_common_members = reduce(np.intersect1d, CMIP5_predictor_choices)

# Driving models for CH202x RCMs
CMIP5_RCM_common_members = ['CNRM-CM5-r1i1p1','CanESM2-r1i1p1','EC-EARTH-r12i1p1',
'EC-EARTH-r1i1p1','HadGEM2-ES-r1i1p1','IPSL-CM5A-MR-r1i1p1','MIROC5-r1i1p1',
'MPI-ESM-LR-r1i1p1','MPI-ESM-LR-r2i1p1','MPI-ESM-LR-r3i1p1','NorESM1-M-r1i1p1']

# From Sobolowski et al. (2023)
# EURO-CORDEX CMIP6 GCM Selection & Ensemble Design: Best Practices and Recommendations.
# Zenodo. https://doi.org/10.5281/zenodo.7673400
CMIP6_RCM_common_members = ['CESM2-r11i1p1f1','CMCC-CM2-SR5-r1i1p1f1',
'CNRM-ESM2-1-r1i1p1f2', 'EC-Earth3-Veg-r1i1p1f1','IPSL-CM6A-LR-r1i1p1f1',
'MIROC6-r1i1p1f1', 'MPI-ESM1-2-HR-r1i1p1f1','NorESM2-MM-r1i1p1f1', 'UKESM1-0-LL-r1i1p1f2']

#################################
## Selecting Spread-i-est Members
#################################

## functions

# normalize for spread
def normalize_spread_component(ds):
    return (ds  - np.mean(ds))/np.std(ds)

# add ensemble member from ICEs/PPEs
def select_spread_maximizing_member(keys,ds_norm,dict_ind):
    # create a dictionary of a model's ensemble member positions
    dict_model = {}
    for ii in range(len(keys)):
        dict_model[keys[ii]] = (ds_norm[0].sel(member=keys[ii]).tas.item(0),ds_norm[1].sel(member=keys[ii]).pr.item(0))

    # determine the closest already-placed-model to each ensemble member
    member_dist = {}
    def choose_furthest_member(mem,dict_model):
        dict_dist = {}
        for key in dict_ind:
            dist = np.linalg.norm(np.array(dict_model[mem]) - np.array(dict_ind[key]))
            dict_dist[key] = dist
        min_key = min(dict_dist, key=dict_dist.get)
        min_value = min(dict_dist.values())
        #print("Lowest value:",mem,min_key,min_value)
        member_dist[mem] = min_value
        return member_dist

    for ii in range(len(keys)):
        member_dist = choose_furthest_member(keys[ii],dict_model)

    # select ensemble member that maximizes overall ensemble spread
    key_choice = max(member_dist, key=member_dist.get)
    dict_ind[key_choice] = (ds_norm[0].sel(member=key_choice).tas.item(0),ds_norm[1].sel(member=key_choice).pr.item(0))
    return dict_ind

def list_for_max_spread(dict_ind):
    mem = list(dict_ind.keys())
    return mem

def CMIP6_spread_maximizing_members(CMIP6_common_members,season_region):
    path ='/net/h2o/climphys/meranna/Data/predictors/spread/'

    if season_region == 'JJA_CEU':
    # select default models
        dsT6 = xr.open_dataset(path+'tas_CMIP6_SSP585_CEU_jja_2041-2060_1995-2014_diff.nc',use_cftime = True)
        dsT6 = dsT6.sel(member=CMIP6_common_members)

        dsPr6 = xr.open_dataset(path+'pr_CMIP6_SSP585_CEU_jja_2041-2060_1995-2014_diff.nc',use_cftime = True)
        dsPr6 = dsPr6.sel(member=CMIP6_common_members)

    if season_region == 'DJF_NEU':
        dsT6 = xr.open_dataset(path+'tas_CMIP6_SSP585_NEU_djf_2041-2060_1995-2014_diff.nc',use_cftime = True)
        dsT6 = dsT6.sel(member=CMIP6_common_members)

        dsPr6 = xr.open_dataset(path+'pr_CMIP6_SSP585_NEU_djf_2041-2060_1995-2014_diff.nc',use_cftime = True)
        dsPr6 = dsPr6.sel(member=CMIP6_common_members)

    if season_region == 'DJF_CEU':
        dsT6 = xr.open_dataset(path+'tas_CMIP6_SSP585_CEU_djf_2041-2060_1995-2014_diff.nc',use_cftime = True)
        dsT6 = dsT6.sel(member=CMIP6_common_members)

        dsPr6 = xr.open_dataset(path+'pr_CMIP6_SSP585_CEU_djf_2041-2060_1995-2014_diff.nc',use_cftime = True)
        dsPr6 = dsPr6.sel(member=CMIP6_common_members)

    targets = [dsT6,dsPr6]

    # normalize targets
    ds_norm = []
    for ds in targets:
        ds_norm.append(normalize_spread_component(ds))

    # fixed ponts - individuals
    keys = ['AWI-CM-1-1-MR-r1i1p1f1', 'CMCC-CM2-SR5-r1i1p1f1',
    'CMCC-ESM2-r1i1p1f1', 'CNRM-CM6-1-HR-r1i1p1f2',
    'E3SM-1-1-r1i1p1f1', 'FGOALS-f3-L-r1i1p1f1', 'GFDL-CM4-r1i1p1f1', 'GFDL-ESM4-r1i1p1f1',
    'GISS-E2-1-G-r1i1p3f1', 'INM-CM4-8-r1i1p1f1', 'INM-CM5-0-r1i1p1f1','KIOST-ESM-r1i1p1f1',
    'NorESM2-MM-r1i1p1f1','TaiESM1-r1i1p1f1']

    # create a dictionary with fixed point keys and position
    dict_ind = {}
    for ii in range(len(keys)):
        dict_ind[keys[ii]] = (ds_norm[0].sel(member=keys[ii]).tas.item(0),ds_norm[1].sel(member=keys[ii]).pr.item(0))

    # determing spread-maximizing member in order, CMIP6
    keys = ['ACCESS-CM2-r1i1p1f1', 'ACCESS-CM2-r2i1p1f1', 'ACCESS-CM2-r3i1p1f1']
    dict_ind = select_spread_maximizing_member(keys,ds_norm,dict_ind)

    keys = ['ACCESS-ESM1-5-r10i1p1f1', 'ACCESS-ESM1-5-r1i1p1f1',
           'ACCESS-ESM1-5-r2i1p1f1', 'ACCESS-ESM1-5-r3i1p1f1',
           'ACCESS-ESM1-5-r4i1p1f1', 'ACCESS-ESM1-5-r5i1p1f1',
           'ACCESS-ESM1-5-r6i1p1f1', 'ACCESS-ESM1-5-r7i1p1f1',
           'ACCESS-ESM1-5-r8i1p1f1', 'ACCESS-ESM1-5-r9i1p1f1']
    dict_ind = select_spread_maximizing_member(keys,ds_norm,dict_ind)

    keys = ['CAS-ESM2-0-r1i1p1f1', 'CAS-ESM2-0-r3i1p1f1']
    dict_ind = select_spread_maximizing_member(keys,ds_norm,dict_ind)

    keys = ['CESM2-WACCM-r1i1p1f1', 'CESM2-WACCM-r2i1p1f1', 'CESM2-WACCM-r3i1p1f1']
    dict_ind = select_spread_maximizing_member(keys,ds_norm,dict_ind)

    keys = ['CESM2-r10i1p1f1', 'CESM2-r11i1p1f1', 'CESM2-r1i1p1f1','CESM2-r2i1p1f1', 'CESM2-r4i1p1f1']
    dict_ind = select_spread_maximizing_member(keys,ds_norm,dict_ind)

    keys = ['CNRM-CM6-1-r1i1p1f2','CNRM-CM6-1-r2i1p1f2',
    'CNRM-CM6-1-r3i1p1f2', 'CNRM-CM6-1-r4i1p1f2',
    'CNRM-CM6-1-r5i1p1f2', 'CNRM-CM6-1-r6i1p1f2']
    dict_ind = select_spread_maximizing_member(keys,ds_norm,dict_ind)

    keys = ['CNRM-ESM2-1-r1i1p1f2','CNRM-ESM2-1-r2i1p1f2', 'CNRM-ESM2-1-r3i1p1f2', 'CNRM-ESM2-1-r4i1p1f2','CNRM-ESM2-1-r5i1p1f2']
    dict_ind = select_spread_maximizing_member(keys,ds_norm,dict_ind)

    keys = ['CanESM5-r10i1p1f1', 'CanESM5-r10i1p2f1',
           'CanESM5-r11i1p1f1', 'CanESM5-r11i1p2f1', 'CanESM5-r12i1p1f1',
           'CanESM5-r12i1p2f1', 'CanESM5-r13i1p1f1', 'CanESM5-r13i1p2f1',
           'CanESM5-r14i1p1f1', 'CanESM5-r14i1p2f1', 'CanESM5-r15i1p1f1',
           'CanESM5-r15i1p2f1', 'CanESM5-r16i1p1f1', 'CanESM5-r16i1p2f1',
           'CanESM5-r17i1p1f1', 'CanESM5-r17i1p2f1', 'CanESM5-r18i1p1f1',
           'CanESM5-r18i1p2f1', 'CanESM5-r19i1p1f1', 'CanESM5-r19i1p2f1',
           'CanESM5-r1i1p1f1', 'CanESM5-r1i1p2f1', 'CanESM5-r20i1p1f1',
           'CanESM5-r20i1p2f1', 'CanESM5-r21i1p1f1', 'CanESM5-r21i1p2f1',
           'CanESM5-r22i1p1f1', 'CanESM5-r22i1p2f1', 'CanESM5-r23i1p1f1',
           'CanESM5-r23i1p2f1', 'CanESM5-r24i1p1f1', 'CanESM5-r24i1p2f1',
           'CanESM5-r25i1p1f1', 'CanESM5-r25i1p2f1', 'CanESM5-r2i1p1f1',
           'CanESM5-r2i1p2f1', 'CanESM5-r3i1p1f1', 'CanESM5-r3i1p2f1',
           'CanESM5-r4i1p1f1', 'CanESM5-r4i1p2f1', 'CanESM5-r5i1p1f1',
           'CanESM5-r5i1p2f1', 'CanESM5-r6i1p1f1', 'CanESM5-r6i1p2f1',
           'CanESM5-r7i1p1f1', 'CanESM5-r7i1p2f1', 'CanESM5-r8i1p1f1',
           'CanESM5-r8i1p2f1', 'CanESM5-r9i1p1f1', 'CanESM5-r9i1p2f1']
    dict_ind = select_spread_maximizing_member(keys,ds_norm,dict_ind)

    keys = ['FGOALS-g3-r1i1p1f1','FGOALS-g3-r2i1p1f1']
    dict_ind = select_spread_maximizing_member(keys,ds_norm,dict_ind)

    keys = ['HadGEM3-GC31-LL-r1i1p1f3','HadGEM3-GC31-LL-r2i1p1f3', 'HadGEM3-GC31-LL-r3i1p1f3','HadGEM3-GC31-LL-r4i1p1f3']
    dict_ind = select_spread_maximizing_member(keys,ds_norm,dict_ind)

    keys = ['HadGEM3-GC31-MM-r1i1p1f3','HadGEM3-GC31-MM-r2i1p1f3', 'HadGEM3-GC31-MM-r3i1p1f3','HadGEM3-GC31-MM-r4i1p1f3']
    dict_ind = select_spread_maximizing_member(keys,ds_norm,dict_ind)

    keys = ['IPSL-CM6A-LR-r14i1p1f1', 'IPSL-CM6A-LR-r1i1p1f1',
            'IPSL-CM6A-LR-r2i1p1f1', 'IPSL-CM6A-LR-r3i1p1f1',
            'IPSL-CM6A-LR-r4i1p1f1', 'IPSL-CM6A-LR-r6i1p1f1']
    dict_ind = select_spread_maximizing_member(keys,ds_norm,dict_ind)

    keys = ['KACE-1-0-G-r2i1p1f1','KACE-1-0-G-r3i1p1f1']
    dict_ind = select_spread_maximizing_member(keys,ds_norm,dict_ind)

    keys = ['MIROC-ES2L-r10i1p1f2','MIROC-ES2L-r1i1p1f2', 'MIROC-ES2L-r2i1p1f2', 'MIROC-ES2L-r3i1p1f2',
    'MIROC-ES2L-r4i1p1f2', 'MIROC-ES2L-r5i1p1f2', 'MIROC-ES2L-r6i1p1f2','MIROC-ES2L-r7i1p1f2', 'MIROC-ES2L-r8i1p1f2', 'MIROC-ES2L-r9i1p1f2']
    dict_ind = select_spread_maximizing_member(keys,ds_norm,dict_ind)

    keys = ['MIROC6-r10i1p1f1', 'MIROC6-r11i1p1f1', 'MIROC6-r12i1p1f1',
           'MIROC6-r13i1p1f1', 'MIROC6-r14i1p1f1', 'MIROC6-r15i1p1f1',
           'MIROC6-r16i1p1f1', 'MIROC6-r17i1p1f1', 'MIROC6-r18i1p1f1',
           'MIROC6-r19i1p1f1', 'MIROC6-r1i1p1f1', 'MIROC6-r20i1p1f1',
           'MIROC6-r21i1p1f1', 'MIROC6-r22i1p1f1', 'MIROC6-r23i1p1f1',
           'MIROC6-r24i1p1f1', 'MIROC6-r25i1p1f1', 'MIROC6-r26i1p1f1',
           'MIROC6-r27i1p1f1', 'MIROC6-r28i1p1f1', 'MIROC6-r29i1p1f1',
           'MIROC6-r2i1p1f1', 'MIROC6-r30i1p1f1', 'MIROC6-r31i1p1f1',
           'MIROC6-r32i1p1f1', 'MIROC6-r33i1p1f1', 'MIROC6-r34i1p1f1',
           'MIROC6-r35i1p1f1', 'MIROC6-r36i1p1f1', 'MIROC6-r37i1p1f1',
           'MIROC6-r38i1p1f1', 'MIROC6-r39i1p1f1', 'MIROC6-r3i1p1f1',
           'MIROC6-r40i1p1f1', 'MIROC6-r41i1p1f1', 'MIROC6-r42i1p1f1',
           'MIROC6-r43i1p1f1', 'MIROC6-r44i1p1f1', 'MIROC6-r45i1p1f1',
           'MIROC6-r46i1p1f1', 'MIROC6-r47i1p1f1', 'MIROC6-r48i1p1f1',
           'MIROC6-r49i1p1f1', 'MIROC6-r4i1p1f1', 'MIROC6-r50i1p1f1',
           'MIROC6-r5i1p1f1', 'MIROC6-r6i1p1f1', 'MIROC6-r7i1p1f1',
           'MIROC6-r8i1p1f1', 'MIROC6-r9i1p1f1']
    dict_ind = select_spread_maximizing_member(keys,ds_norm,dict_ind)

    keys = ['MPI-ESM1-2-HR-r1i1p1f1',
            'MPI-ESM1-2-HR-r2i1p1f1']
    dict_ind = select_spread_maximizing_member(keys,ds_norm,dict_ind)

    keys = ['MPI-ESM1-2-LR-r10i1p1f1',
           'MPI-ESM1-2-LR-r1i1p1f1', 'MPI-ESM1-2-LR-r2i1p1f1',
           'MPI-ESM1-2-LR-r3i1p1f1', 'MPI-ESM1-2-LR-r4i1p1f1',
           'MPI-ESM1-2-LR-r5i1p1f1', 'MPI-ESM1-2-LR-r6i1p1f1',
           'MPI-ESM1-2-LR-r7i1p1f1', 'MPI-ESM1-2-LR-r8i1p1f1',
           'MPI-ESM1-2-LR-r9i1p1f1']
    dict_ind = select_spread_maximizing_member(keys,ds_norm,dict_ind)

    keys = ['MRI-ESM2-0-r1i1p1f1', 'MRI-ESM2-0-r1i2p1f1']
    dict_ind = select_spread_maximizing_member(keys,ds_norm,dict_ind)

    keys = ['NESM3-r1i1p1f1', 'NESM3-r2i1p1f1']
    dict_ind = select_spread_maximizing_member(keys,ds_norm,dict_ind)

    keys = ['UKESM1-0-LL-r1i1p1f2', 'UKESM1-0-LL-r2i1p1f2',
            'UKESM1-0-LL-r3i1p1f2', 'UKESM1-0-LL-r4i1p1f2', 'UKESM1-0-LL-r8i1p1f2']
    dict_ind = select_spread_maximizing_member(keys,ds_norm,dict_ind)

    mem_out = list_for_max_spread(dict_ind)
    return mem_out

def CMIP5_spread_maximizing_members(CMIP5_common_members,season_region):
    path ='/net/h2o/climphys/meranna/Data/predictors/spread/'

    if season_region == 'JJA_CEU':
    # select default models
        dsT5 = xr.open_dataset(path+'tas_CMIP5_rcp85_CEU_jja_2041-2060_1995-2014_diff.nc',use_cftime = True)
        dsT5 = dsT5.sel(member=CMIP5_common_members)

        dsPr5 = xr.open_dataset(path+'pr_CMIP5_rcp85_CEU_jja_2041-2060_1995-2014_diff.nc',use_cftime = True)
        dsPr5 = dsPr5.sel(member=CMIP5_common_members)

    if season_region == 'DJF_NEU':
        dsT5 = xr.open_dataset(path+'tas_CMIP5_rcp85_NEU_djf_2041-2060_1995-2014_diff.nc',use_cftime = True)
        dsT5 = dsT5.sel(member=CMIP5_common_members)

        dsPr5 = xr.open_dataset(path+'pr_CMIP5_rcp85_NEU_djf_2041-2060_1995-2014_diff.nc',use_cftime = True)
        dsPr5 = dsPr5.sel(member=CMIP5_common_members)

    if season_region == 'DJF_CEU':
        dsT5 = xr.open_dataset(path+'tas_CMIP5_rcp85_CEU_djf_2041-2060_1995-2014_diff.nc',use_cftime = True)
        dsT5 = dsT5.sel(member=CMIP5_common_members)

        dsPr5 = xr.open_dataset(path+'pr_CMIP5_rcp85_CEU_djf_2041-2060_1995-2014_diff.nc',use_cftime = True)
        dsPr5 = dsPr5.sel(member=CMIP5_common_members)

    targets = [dsT5,dsPr5]


    # normalize targets
    ds_norm = []
    for ds in targets:
        ds_norm.append(normalize_spread_component(ds))

    # fixed ponts - individuals
    keys = ['ACCESS1-0-r1i1p1', 'ACCESS1-3-r1i1p1','GFDL-CM3-r1i1p1', 'GFDL-ESM2G-r1i1p1',
    'GFDL-ESM2M-r1i1p1','IPSL-CM5A-MR-r1i1p1', 'IPSL-CM5B-LR-r1i1p1',
    'MIROC-ESM-r1i1p1','MPI-ESM-MR-r1i1p1', 'MRI-CGCM3-r1i1p1', 'NorESM1-M-r1i1p1',
    'NorESM1-ME-r1i1p1', 'bcc-csm1-1-m-r1i1p1', 'bcc-csm1-1-r1i1p1',
    'inmcm4-r1i1p1']

    # create a dictionary with fixed point keys and position
    dict_ind = {}
    for ii in range(len(keys)):
        dict_ind[keys[ii]] = (ds_norm[0].sel(member=keys[ii]).tas.item(0),ds_norm[1].sel(member=keys[ii]).pr.item(0))

    # determing spread-maximizing member in order, CMIP5
    keys = ['CCSM4-r1i1p1', 'CCSM4-r2i1p1','CCSM4-r3i1p1', 'CCSM4-r4i1p1', 'CCSM4-r5i1p1', 'CCSM4-r6i1p1']
    dict_ind = select_spread_maximizing_member(keys,ds_norm,dict_ind)

    keys = ['CESM1-CAM5-r1i1p1', 'CESM1-CAM5-r2i1p1', 'CESM1-CAM5-r3i1p1']
    dict_ind = select_spread_maximizing_member(keys,ds_norm,dict_ind)

    keys = ['CNRM-CM5-r10i1p1', 'CNRM-CM5-r1i1p1', 'CNRM-CM5-r2i1p1','CNRM-CM5-r4i1p1', 'CNRM-CM5-r6i1p1']
    dict_ind = select_spread_maximizing_member(keys,ds_norm,dict_ind)

    keys = ['CSIRO-Mk3-6-0-r10i1p1',
    'CSIRO-Mk3-6-0-r1i1p1', 'CSIRO-Mk3-6-0-r2i1p1', 'CSIRO-Mk3-6-0-r3i1p1',
    'CSIRO-Mk3-6-0-r4i1p1', 'CSIRO-Mk3-6-0-r5i1p1', 'CSIRO-Mk3-6-0-r6i1p1',
    'CSIRO-Mk3-6-0-r7i1p1', 'CSIRO-Mk3-6-0-r8i1p1', 'CSIRO-Mk3-6-0-r9i1p1']
    dict_ind = select_spread_maximizing_member(keys,ds_norm,dict_ind)

    keys = ['CanESM2-r1i1p1', 'CanESM2-r2i1p1', 'CanESM2-r3i1p1', 'CanESM2-r4i1p1','CanESM2-r5i1p1']
    dict_ind = select_spread_maximizing_member(keys,ds_norm,dict_ind)

    keys = ['GISS-E2-H-r1i1p1', 'GISS-E2-H-r1i1p2','GISS-E2-H-r1i1p3', 'GISS-E2-H-r2i1p1', 'GISS-E2-H-r2i1p3']
    dict_ind = select_spread_maximizing_member(keys,ds_norm,dict_ind)

    keys = ['GISS-E2-R-r1i1p1', 'GISS-E2-R-r1i1p2', 'GISS-E2-R-r1i1p3','GISS-E2-R-r2i1p1', 'GISS-E2-R-r2i1p3']
    dict_ind = select_spread_maximizing_member(keys,ds_norm,dict_ind)

    keys = ['HadGEM2-ES-r1i1p1','HadGEM2-ES-r2i1p1', 'HadGEM2-ES-r3i1p1', 'HadGEM2-ES-r4i1p1']
    dict_ind = select_spread_maximizing_member(keys,ds_norm,dict_ind)

    ## skip 'IPSL-CM5A-LR-r2i1p1' (0.6) in favor of choosing 'IPSL-CM5A-LR-r1i1p1' (0.55)
    keys = ['IPSL-CM5A-LR-r1i1p1', 'IPSL-CM5A-LR-r3i1p1','IPSL-CM5A-LR-r4i1p1']
    dict_ind = select_spread_maximizing_member(keys,ds_norm,dict_ind)

    keys = ['MIROC5-r1i1p1', 'MIROC5-r2i1p1', 'MIROC5-r3i1p1']
    dict_ind = select_spread_maximizing_member(keys,ds_norm,dict_ind)

    keys = ['MPI-ESM-LR-r1i1p1', 'MPI-ESM-LR-r2i1p1', 'MPI-ESM-LR-r3i1p1']
    dict_ind = select_spread_maximizing_member(keys,ds_norm,dict_ind)

    mem_out = list_for_max_spread(dict_ind)
    return mem_out

def CMIP5_RCM_spread_maximizing_members(CMIP5_RCM_common_members,season_region):
    path ='/net/h2o/climphys/meranna/Data/predictors/spread/'

    if season_region == 'JJA_CEU':
    # select default models
        dsT5 = xr.open_dataset(path+'tas_CMIP5_rcp85_CEU_jja_2041-2060_1995-2014_diff.nc',use_cftime = True)
        dsT5 = dsT5.sel(member=CMIP5_RCM_common_members)

        dsPr5 = xr.open_dataset(path+'pr_CMIP5_rcp85_CEU_jja_2041-2060_1995-2014_diff.nc',use_cftime = True)
        dsPr5 = dsPr5.sel(member=CMIP5_RCM_common_members)

    if season_region == 'DJF_NEU':
        dsT5 = xr.open_dataset(path+'tas_CMIP5_rcp85_NEU_djf_2041-2060_1995-2014_diff.nc',use_cftime = True)
        dsT5 = dsT5.sel(member=CMIP5_RCM_common_members)

        dsPr5 = xr.open_dataset(path+'pr_CMIP5_rcp85_NEU_djf_2041-2060_1995-2014_diff.nc',use_cftime = True)
        dsPr5 = dsPr5.sel(member=CMIP5_RCM_common_members)

    if season_region == 'DJF_CEU':
        dsT5 = xr.open_dataset(path+'tas_CMIP5_rcp85_CEU_djf_2041-2060_1995-2014_diff.nc',use_cftime = True)
        dsT5 = dsT5.sel(member=CMIP5_RCM_common_members)

        dsPr5 = xr.open_dataset(path+'pr_CMIP5_rcp85_CEU_djf_2041-2060_1995-2014_diff.nc',use_cftime = True)
        dsPr5 = dsPr5.sel(member=CMIP5_RCM_common_members)

    targets = [dsT5,dsPr5]

    # normalize targets
    ds_norm = []
    for ds in targets:
        ds_norm.append(normalize_spread_component(ds))

    # fixed ponts - individuals
    keys = ['CNRM-CM5-r1i1p1','CanESM2-r1i1p1','HadGEM2-ES-r1i1p1','IPSL-CM5A-MR-r1i1p1',
    'MIROC5-r1i1p1','NorESM1-M-r1i1p1']

    # create a dictionary with fixed point keys and position
    dict_ind = {}
    for ii in range(len(keys)):
        dict_ind[keys[ii]] = (ds_norm[0].sel(member=keys[ii]).tas.item(0),ds_norm[1].sel(member=keys[ii]).pr.item(0))

    # determing spread-maximizing member in order, CMIP5
    keys = ['EC-EARTH-r12i1p1','EC-EARTH-r1i1p1']
    dict_ind = select_spread_maximizing_member(keys,ds_norm,dict_ind)

    keys = ['MPI-ESM-LR-r1i1p1','MPI-ESM-LR-r2i1p1','MPI-ESM-LR-r3i1p1']
    dict_ind = select_spread_maximizing_member(keys,ds_norm,dict_ind)

    mem_out = list_for_max_spread(dict_ind)
    return mem_out
