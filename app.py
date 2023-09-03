import numpy as np
import genie_script as genie
import cross_sections as cs

# set the threshold for code checks
code_check_threshold = 0.9

structure_config = genie.setup_model()
sections = cs.get_available_sections()

# initialize the optimized structure configuration
optimized_structure_config = structure_config

# this is the optimization process from gafra
best_code_check = 0.0
for i, member in enumerate(structure_config):
    for section in sections:
        # set one section at one member
        member['member'].section = section
        # run genie analysis and return list of code checks
        code_checks = genie.run_analysis()
        # check if code checks are valid; reject cross section if not
        if any(code_checks) > code_check_threshold:
            pass
        else:
            # code checks are ok
            # continue to check if code checks are better than previous best
            # HERE WE OPTIMIZE BASED ON THE MEAN OF THE CODE CHECKS
            # ...OR SHOULD WE OPTIMIZE BASED ON WEIGHT OF THE STRUCTURE?
            
            # compute the mean of the code checks
            if np.mean(code_checks) > best_code_check_mean:
                # if better than previous best, save the section to the configuration
                optimized_structure_config[i]['member'].section = section
                # save the best mean code check value
                best_code_check_mean = np.mean(code_checks)
            
            