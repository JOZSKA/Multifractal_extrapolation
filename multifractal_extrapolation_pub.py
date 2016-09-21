# Author: Jozef Skakala, PML, 2016 
# This is the core function for the extrapolation. Plug in field at larger scales ('field') and obtain returned field at lower scales (determined by the iteraion exponent: `n_iterations').  Besides the field distribution input and number of iterations, other optional arguments are 'latitudes', 'momenta_flux', 'momenta_inc', 'max_scale', 'min_scale', 'scale_coeff', 'mask', 'scales_inc' and 'ratio_bound'. If the optional arguments are skipped, the arguments take their default values from the multifractal_parameter_pub module. The 'latitudes' argument is supplied to calculate the physical distance from the longitudal (spherical) coordinate distance. It can be also used to reflect on grid pixels that have unequal length in longitude and latitude directions. The increments scaling calculation can be computationally costly and therefore one can choose optimal range of scales for the analysis through the 'scales_inc' argument. It can be argued that the multiplicative (log-homogeneous) cascade from the default settings (pa.scales(...)) is for the increments scaling analysis far from optimal. One for example might prefer to use homogeneously spread scales with a suitable scaling gap. The additional arguments (as listed before) are separately introduced as optional in both multifractal_extrapolation_pub and multifractal_class_pub, instead of just being passed as the essential arguments to the multifractal_class_pub. The reason for this is that multifractal_class_pub stands as a separate computational tool in the situations when one is interested only in the scaling analysis and not in the field extrapolation.

import numpy as np
import multifractal_basic_functions_pub as mbf
import multifractal_extrapolate_functions_pub as mef
from multifractal_class_pub import multifractals
import multifractal_parameter_values_pub as pa

def field_extrapolation(field, n_iterations, **kwargs):

    if 'latitudes' in kwargs:
        latitudes = kwargs['latitudes']
    else:
        latitudes = np.zeros(np.shape(field))
       
    if 'momenta_flux' in kwargs:
        momenta_flux = kwargs['momenta_flux']
    else:
        momenta_flux = pa.flux_momenta()

    if 'momenta_inc' in kwargs:
        momenta_inc = kwargs['momenta_inc']
    else:
        momenta_inc = pa.inc_momenta()

    if 'max_scale' in kwargs:
        max_scale = kwargs['max_scale']
    else:
        max_scale = pa.max_scale() 
                 
    if 'min_scale' in kwargs:
        min_scale = kwargs['min_scale']
    else:
        min_scale = pa.min_scale() 

    if 'scale_coeff' in kwargs:
        scale_coeff = kwargs['scale_coeff']
    else:
        scale_coeff = pa.scale_coeff()

    if 'mask' in kwargs:
        mask = kwargs['mask']
    else:
        mask = pa.masking_value()  

    if 'scales_inc' in kwargs:
        scales_inc = kwargs['scales_inc']
    else:
        scales_inc = pa.scales(max_scale, min_scale, scale_coeff)

    if 'ratio_bound' in kwargs:
        ratio_bound = kwargs['ratio_bound']
    else:
        ratio_bound = pa.ratio_bound()


    field_multifractal = multifractals(field, latitudes = latitudes, momenta_flux = momenta_flux, momenta_inc = momenta_inc, max_scale = max_scale, min_scale = min_scale, scale_coeff = scale_coeff, mask = mask, scales_inc = scales_inc)    # Calculate the multifractal scaling of the field
    parameters = field_multifractal.UM_parameters()  # Extract the UM parameters
    fluxes = field_multifractal.fluxes()  # Extract the fluxes
    factor = parameters[4]*(1/2.0**n_iterations)**parameters[0]   # the factor that relates fluctuations to fluxes
    

    fluxes_extrapolated = mef.fluxes_extrapolate(fluxes, n_iterations, parameters, mask)   # Extrapolate fluxes

    field_scaled_down = mef.smoothen(mef.lower_resolution(field, 2**n_iterations), 2**n_iterations, 2**n_iterations, 2.0, mask)  # Get the smoothen version of the field on the lower scale

    field_extrapolated = mef.fluctuations_distribute(field_scaled_down, fluxes_extrapolated, factor, ratio_bound, mask)  # Distribute the field fluctuations on the lower scale using the 1. fluxes and 2. smoothened field .

    return field_extrapolated
