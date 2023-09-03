# This library shall be used from GaFra to select appropriate section sizes for the code checks – Parameter 1
# THERE MUST BE a Geinie python function that returns a list of all available sections
# For now we jsut use a custom list    

def get_available_sections():
    return list(UB_127x76x13,
                UB_127x76x13,
                UB_127x76x13,
                UB_152x89x16,
                UB_152x89x16,
                UB_152x89x16,
                UC_203x203x60,
                UC_203x203x60,
                UB_203x133x25,
                UB_203x133x25,
                UB_203x133x25)


