import streamlit as st
import pandas as pd
from evolution_bot import EvolutionSimulationBot

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

st.header("3. Add Starting Population")

st.subheader("Option A: Upload CSV File")
uploaded_file = st.file_uploader("Upload population CSV", type="csv")

if uploaded_file is not None:
    try:
        df = pd.read_csv(uploaded_file)
        st.write("Preview of data:")
        st.dataframe(df)
        
        if st.button("Load Population from CSV"):
            if not bot.trait_definitions:
                st.error("Define traits first!")
            else:
                for idx, row in df.iterrows():
                    individual_id = row['ID']
                    genotypes = {}
                    for trait in bot.trait_definitions.keys():
                        allele1 = row[f'{trait}_allele1']
                        allele2 = row[f'{trait}_allele2']
                        genotypes[trait] = (allele1, allele2)
                    bot.add_individual(individual_id, genotypes)
                st.success(f"Loaded {len(df)} individuals!")
    except Exception as e:
        st.error(f"Error reading CSV: {e}")

st.subheader("Option B: Add Individuals Manually")
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
    if not bot.trait_definitions:
        st.error("Define traits first!")
    elif genotypes_dict:
        st.write(bot.add_individual(individual_id, genotypes_dict))
    else:
        st.warning("Select alleles!")

st.info(f"Population: {len(bot.population)}")

if st.button("Show Population"):
    st.write(bot.get_population_summary())

st.header("4. Download CSV Template")
st.markdown("Download template to fill in your individuals:")

template_data = {
    'ID': ['Fox1', 'Fox2', 'Fox3'],
    'fur_color_allele1': ['W', 'w', 'W'],
    'fur_color_allele2': ['w', 'w', 'W']
}
template_df = pd.DataFrame(template_data)
csv = template_df.to_csv(index=False)
st.download_button(label="Download CSV Template", data=csv, file_name="population_template.csv", mime="text/csv")

st.header("5. Run Generation")
if st.button("Run Generation"):
    if not bot.trait_definitions:
        st.error("Define traits first!")
    elif len(bot.population) < 2:
        st.error("Need at least 2 individuals!")
    else:
        st.write(bot.random_mating())
        st.write(bot.apply_beneficial_mutation())
        st.write(bot.apply_survival_filtering())

st.header("6. Results")

col1, col2 = st.columns(2)

with col1:
    if st.button("Show Population as Table"):
        population_data = []
        for ind_id, individual in sorted(bot.population.items()):
            row = {'ID': ind_id, 'Status': 'Alive' if individual.is_alive else 'Dead', 'Generation': individual.generation}
            for trait, (allele1, allele2) in individual.genotypes.items():
                row[f'{trait}_genotype'] = f"{allele1}{allele2}"
            for trait, phenotype in individual.phenotypes.items():
                row[f'{trait}_phenotype'] = phenotype
            population_data.append(row)
        
        results_df = pd.DataFrame(population_data)
        st.dataframe(results_df)
        
        csv_results = results_df.to_csv(index=False)
        st.download_button(label="Download Results as CSV", data=csv_results, file_name="population_results.csv", mime="text/csv")

with col2:
    if st.button("Show History"):
        if bot.population_history:
            history_data = []
            for gen, size in sorted(bot.population_history.items()):
                history_data.append({'Generation': gen, 'Population Size': size})
            history_df = pd.DataFrame(history_data)
            st.dataframe(history_df)
            
            csv_history = history_df.to_csv(index=False)
            st.download_button(label="Download History as CSV", data=csv_history, file_name="population_history.csv", mime="text/csv")

if bot.mutation_event:
    st.header("Mutation Details")
    mutation_data = {
        'Individual': bot.mutation_event['individual'],
        'Trait': bot.mutation_event['trait'],
        'Old Genotype': bot.mutation_event['old_genotype'],
        'New Genotype': bot.mutation_event['new_genotype'],
        'Habitat': bot.mutation_event['habitat']
    }
    mutation_df = pd.DataFrame([mutation_data])
    st.dataframe(mutation_df)
    
    csv_mutation = mutation_df.to_csv(index=False)
    st.download_button(label="Download Mutation Details as CSV", data=csv_mutation, file_name="mutation_details.csv", mime="text/csv")

