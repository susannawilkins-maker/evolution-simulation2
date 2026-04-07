import streamlit as st

st.set_page_config(page_title="Evolution Simulation", layout="wide")
st.title("Classroom Evolution Simulation")

if 'bot' not in st.session_state:
    st.session_state.bot = EvolutionSimulationBot()

bot = st.session_state.bot

st.header("1. Setup Habitat")
habitat = st.text_input("Enter habitat:", "Arctic Tundra")
if st.button("Set Habitat"):
    st.write(bot.setup_habitat(habitat))

st.header("2. Define Traits")
trait_name = st.text_input("Trait name:", "fur_color")
dom_allele = st.text_input("Dominant allele:", "W")
rec_allele = st.text_input("Recessive allele:", "w")
dom_phenotype = st.text_input("Dominant phenotype:", "White fur")
rec_phenotype = st.text_input("Recessive phenotype:", "Brown fur")

if st.button("Add Trait"):
    st.write(bot.define_trait(trait_name, dom_allele, rec_allele, dom_phenotype, rec_phenotype))

st.info(f"Traits: {list(bot.trait_definitions.keys())}")

st.header("3. Add Individuals")
individual_id = st.text_input("Individual ID:", "Fox1")
genotypes_dict = {}

if bot.trait_definitions:
    for trait in bot.trait_definitions.keys():
        col1, col2 = st.columns(2)
        with col1:
            a1 = st.selectbox(f"{trait} Allele 1:", [bot.trait_definitions[trait]['dominant_allele'], bot.trait_definitions[trait]['recessive_allele']], key=f"{trait}_a1")
        with col2:
            a2 = st.selectbox(f"{trait} Allele 2:", [bot.trait_definitions[trait]['dominant_allele'], bot.trait_definitions[trait]['recessive_allele']], key=f"{trait}_a2")
        genotypes_dict[trait] = (a1, a2)

if st.button("Add Individual"):
    if genotypes_dict:
        st.write(bot.add_individual(individual_id, genotypes_dict))
    else:
        st.warning("Define traits first!")

st.info(f"Population: {len(bot.population)}")

if st.button("Show Population"):
    st.write(bot.get_population_summary())

st.header("4. Run Generation")
if st.button("Run Generation"):
    if len(bot.population) < 2:
        st.error("Need at least 2 individuals!")
    else:
        st.write(bot.random_mating())
        st.write(bot.apply_beneficial_mutation())
        st.write(bot.apply_survival_filtering())

st.header("5. Results")
col1, col2 = st.columns(2)
with col1:
    if st.button("Show After Survival"):
        st.write(bot.get_population_summary())
with col2:
    if st.button("Show History"):
        if bot.population_history:
            for gen, size in sorted(bot.population_history.items()):
                st.write(f"Gen {gen}: {size}")

if bot.mutation_event:
    st.header("Mutation Details")
    st.json(bot.mutation_event)

