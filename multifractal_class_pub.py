
# Jozef Skakala, PML, 2016.

# Here is the class that has a distribution ('field' argument) as an input and returns the complete multifractal information about the distribution. It computes the UM scaling using all the functions defined in the `multifractal_scaling_essential_pub' module. The names of the attributes are self-explanatory, perhaps with the exception of 'K', which is the standard notation for the moment scaling function. Besides the field distribution input, other optional arguments are 'latitudes', 'momenta_flux', 'momenta_inc', 'max_scale', 'min_scale', 'scale_coeff', 'mask'. If the optional arguments are skipped, the arguments take their default values from the multifractal_parameter_pub module. The 'latitudes' argument is supplied to calculate the physical distance from the longitudal (spherical) coordinate distance. It can be also used to reflect on grid pixels that have unequal length in longitude and latitude directions.



import numpy as np
import multifractal_scaling_essential_pub as mse
import multifractal_parameter_values_pub as pa




class multifractals:

    def __init__(self, field, **kwargs):
            
        self.field = field

#If the optional arguments are omitted, take the default values..

        if 'latitudes' in kwargs:          
            latitudes = kwargs['latitudes']
        else:
            latitudes = np.zeros(np.shape(self.field))

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

        self.description = "Field with multifractal properties - the subject to the analysis."
        self.author = "JS"

# Provides the multifractal scaling calculation..

        (self.field_inc_scaling, self.scales_inc) = mse.scaling_increments(self.field, momenta_inc, max_scale, min_scale, scale_coeff, latitudes, mask)          

        self.flux = mse.fluxes(self.field, 1.0, latitudes, mask)

        (self.flux_scaling, self.scales_flux) = mse.scaling(self.flux, momenta_flux, max_scale, min_scale, scale_coeff, 1.0, 'moment', latitudes, mask)  


        (self.K, self.parameters) = mse.UM_parameters(self.flux_scaling, self.field_inc_scaling, self.scales_flux, self.scales_inc, momenta_flux, momenta_inc)

# The UM_parameters contains: [H, alpha, C_1, outer scale of process, fluctuations proportionality constant, UM fit error]. Please note that the outer_scale calculated through the UM_parameters function is in the units of the regional scale.

        

    def fluxes(self):
        return self.flux

    def increments_scaling(self):
        return self.field_inc_scaling

    def fluxes_scaling(self):
        return self.flux_scaling

    def UM_parameters(self):
        return self.parameters

    def scales_increments(self):    
        return self.scales_inc

    def scales_fluxes(self):
        return self.scales_flux     

    def moment_scaling_function(self):
        return self.K
