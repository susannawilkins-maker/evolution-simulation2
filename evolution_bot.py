import streamlit as st
from evolution_bot import EvolutionSimulationBot

st.set_page_config(page_title="🧬 Evolution Simulation", layout="wide")

st.title("🧬 Classroom Evolution Simulation")
st.markdown("**Simulate natural selection, mutations, and inheritance in real-time!**")
st.markdown("---")

if 'bot' not in st.session_state:
    st.session_state.bot = EvolutionSimulationBot()

bot = st.session_state.bot

st.header("1️⃣ Setup Habitat")

habitat = st.text_input("Enter habitat:", "Arctic Tundra")

if st.button("Set Habitat"):
    result = bot.setup_habitat(habitat)
    st.success(result)

st.header("2️⃣ Define Traits (Complete Dominance)")

st.markdown("Define each trait your population will have.")

trait_name = st.text_input("Trait name (e.g., 'fur_color'):", "fur_color")
dom_allele = st.text_input("Dominant allele (UPPERCASE):", "W")
rec_allele = st.text_input("Recessive allele (lowercase):", "w")
dom_phenotype = st.text_input("Dominant phenotype:", "White fur")
rec_phenotype = st.text_input("Recessive phenotype:", "Brown fur")

if st.button("Add Trait"):
    result = bot.define_trait(trait_name, dom_allele, rec_allele, dom_phenotype, rec_phenotype)
    st.success(result)

st.info(f"Traits defined so far: {list(bot.trait_definitions.keys())}")

st.header("3️⃣ Add Starting Population")

st.markdown("Add individuals with their genotypes for each trait.")

individual_id = st.text_input("Individual name/ID:", "Fox1")

genotypes_dict = {}
if bot.trait_definitions:
    for trait in bot.trait_definitions.keys():
        col1, col2 = st.columns(2)
        with col1:
            allele1 = st.selectbox(f"{trait} - Allele 1:", 
                                  [bot.trait_definitions[trait]['dominant_allele'],
                                   bot.trait_definitions[trait]['recessive_allele']],
                                  key=f"{trait}_a1")
        with col2:
            allele2 = st.selectbox(f"{trait} - Allele 2:",
                                  [bot.trait_definitions[trait]['dominant_allele'],
                                   bot.trait_definitions[trait]['recessive_allele']],
                                  key=f"{trait}_a2")
        genotypes_dict[trait] = (allele1, allele2)

if st.button("Add Individual"):
    if genotypes_dict:
        result = bot.add_individual(individual_id, genotypes_dict)
        st.success(result)
    else:
        st.warning("Define traits first!")

st.info(f"Population size: {len(bot.population)}")

if st.button("Show Current Population"):
    st.write(bot.get_population_summary())

st.header("4️⃣ Run Generation Cycle")

st.markdown("**Cycle includes:**\n1. Random mating (2 offspring per pair)\n2. Beneficial mutation\n3. Survival filtering")

if st.button("▶️ Run Generation", key="run_gen"):
    if len(bot.population) < 2:
        st.error("❌ Need at least 2 individuals to start!")
    else:
        st.subheader("🔗 Step 1: Random Mating")
        mating_result = bot.random_mating()
        st.write(mating_result)
        
        st.subheader("🧬 Step 2: Beneficial Mutation")
        mutation_result = bot.apply_beneficial_mutation()
        st.write(mutation_result)
        
        st.subheader("⚔️ Step 3: Survival Filtering")
        survival_result = bot.apply_survival_filtering()
        st.write(survival_result)

st.header("5️⃣ Results")

col1, col2 = st.columns(2)

with col1:
    if st.button("📊 Show Population After Survival"):
        st.write(bot.get_population_summary())

with col2:
    if st.button("📈 Show Population History"):
        if bot.population_history:
            st.write("**Population Size by Generation:**")
            for gen, size in sorted(bot.population_history.items()):
                st.write(f"Generation {gen}: {size} individuals")
        else:
            st.info("Run a generation first!")

if bot.mutation_event:
    st.header("6️⃣ Mutation Details")
    st.json(bot.mutation_event)

if bot.mating_events:
    st.header("7️⃣ Mating Pairs")
    for event in bot.mating_events:
        st.write(f"**{event.parent1_id}** × **{event.parent2_id}** → {event.offspring_ids}")

st.header("📚 Learning Concepts")

with st.expander("What is Natural Selection?"):
    st.write("""
    **Natural Selection** is the process where:
    
    1. **Mutations create variation** — random changes in DNA
    2. **Some traits fit the habitat better** — organisms with beneficial traits survive more
    3. **Beneficial traits increase over generations** — because more organisms with them survive to reproduce
    
    **Key point:** The environment doesn't *cause* mutations. It *selects* which organisms survive.
    """)

with st.expander("Why is the mutation 75% survival?"):
    st.write("""
    In this simulation:
    - **Normal individuals:** 50% survival chance
    - **Mutant individual:** 75% survival chance
    
    This represents a **beneficial mutation** that helps the organism survive in its habitat.
    
    But survival is still **probabilistic** — even beneficial traits can be lost by chance!
    """)

with st.expander("Why does population size fluctuate?"):
    st.write("""
    Population size changes because:
    
    1. **Mating adds offspring** — each pair makes 2 babies
    2. **Survival filtering removes individuals** — random chance determines who lives/dies
    
    This shows **real evolution** — it's not smooth or predictable!
    
    **Possible outcomes:**
    - Population grows (more survive)
    - Population shrinks (more die)
    - Beneficial trait is lost by chance (even though it's beneficial!)
    - Genetic bottleneck (few survivors = low diversity)
    """)

with st.expander("Complete Dominance"):
    st.write("""
    **Complete dominance** means:
    - If you have even ONE dominant allele → you show the dominant phenotype
    - You only show the recessive phenotype with TWO recessive alleles
    
    **Examples:**
    - WW = White fur (homozygous dominant)
    - Ww = White fur (heterozygous - dominant masks recessive)
    - ww = Brown fur (homozygous recessive)
    """)

st.markdown("---")
st.markdown("*Made for teaching MS-LS3-1, MS-LS3-2, MS-LS4-4, MS-LS4-6*")

