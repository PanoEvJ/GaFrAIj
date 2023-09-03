import setup_model
import cross_sections as cs

members = setup_model()
sections = cs.get_available_sections()

# this is the optimization process from gafra
for member in members:
    for section in sections:
        member.section = section;

        # run genie analysis