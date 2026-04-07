import random
from typing import List, Dict, Tuple, Set
from collections import Counter
from dataclasses import dataclass, field
from enum import Enum

@dataclass
class Individual:
    """Represents a single organism in the population."""
    id: str
    genotypes: Dict[str, Tuple[str, str]]
    phenotypes: Dict[str, str]
    generation: int
    parents: Tuple[str, str] = None
    has_mutation: bool = False
    mutation_info: Dict = field(default_factory=dict)
    is_alive: bool = True
    survival_rate: float = 0.5

@dataclass
class MatingEvent:
    """Records a mating pair and their offspring."""
    parent1_id: str
    parent2_id: str
    offspring_ids: List[str]

class EvolutionSimulationBot:
    """
    Classroom Evolution Simulation
    Teaches MS-LS3-1, MS-LS3-2, MS-LS4-4, MS-LS4-6
    
    Students input a population, the bot simulates:
    1. Random mating (no self-mating)
    2. Mendelian inheritance with complete dominance
    3. One beneficial mutation event
    4. Survival based on phenotype-habitat fit
    """
    
    def __init__(self):
        self.population = {}
        self.habitat = None
        self.trait_definitions = {}
        self.generation = 0
        self.mating_events = []
        self.mutation_event = None
        self.survival_records = []
        self.population_history = {}
    
    def setup_habitat(self, habitat: str) -> str:
        """Set the habitat for the simulation."""
        self.habitat = habitat.strip()
        return f"✓ Habitat set: **{self.habitat}**\n\nNow define traits and starting population."
    
    def define_trait(self, trait_name: str, dominant_allele: str, recessive_allele: str,
                     dominant_phenotype: str, recessive_phenotype: str) -> str:
        """Define a trait with complete dominance."""
        self.trait_definitions[trait_name] = {
            'dominant_allele': dominant_allele.upper(),
            'recessive_allele': recessive_allele.lower(),
            'dominant_phenotype': dominant_phenotype,
            'recessive_phenotype': recessive_phenotype
        }
        
        return (f"✓ Trait defined: **{trait_name}**\n"
                f"  • Dominant: {dominant_allele} → {dominant_phenotype}\n"
                f"  • Recessive: {recessive_allele} → {recessive_phenotype}")
    
    def add_individual(self, individual_id: str, genotypes: Dict[str, Tuple[str, str]]) -> str:
        """Add an individual to the starting population."""
        for trait, (allele1, allele2) in genotypes.items():
            if trait not in self.trait_definitions:
                return f"❌ Error: Trait '{trait}' not defined!"
        
        phenotypes = self._calculate_phenotypes(genotypes)
        
        individual = Individual(
            id=individual_id,
            genotypes=genotypes,
            phenotypes=phenotypes,
            generation=0,
            is_alive=True,
            survival_rate=0.5
        )
        
        self.population[individual_id] = individual
        
        return (f"✓ Added {individual_id}:\n"
                f"  Genotypes: {genotypes}\n"
                f"  Phenotypes: {phenotypes}")
    
    def _calculate_phenotypes(self, genotypes: Dict[str, Tuple[str, str]]) -> Dict[str, str]:
        """Calculate phenotypes from genotypes using complete dominance."""
        phenotypes = {}
        
        for trait, (allele1, allele2) in genotypes.items():
            trait_def = self.trait_definitions[trait]
            dom_allele = trait_def['dominant_allele']
            
            if allele1 == dom_allele or allele2 == dom_allele:
                phenotypes[trait] = trait_def['dominant_phenotype']
            else:
                phenotypes[trait] = trait_def['recessive_phenotype']
        
        return phenotypes
    
    def get_population_summary(self) -> str:
        """Display current population."""
        if not self.population:
            return "Population is empty!"
        
        summary = f"\n{'='*70}\n"
        summary += f"📊 CURRENT POPULATION (Generation {self.generation})\n"
        summary += f"{'='*70}\n"
        summary += f"Total individuals: {len(self.population)}\n"
        summary += f"Alive: {sum(1 for ind in self.population.values() if ind.is_alive)}\n\n"
        
        for ind_id, individual in sorted(self.population.items()):
            status = "✅" if individual.is_alive else "❌"
            mutation_mark = "🧬 MUTATED" if individual.has_mutation else ""
            
            summary += f"{status} **{ind_id}** {mutation_mark}\n"
            
            for trait, (allele1, allele2) in individual.genotypes.items():
                phenotype = individual.phenotypes[trait]
                summary += f"   {trait}: {allele1}{allele2} → {phenotype}\n"
            
            summary += f"   Survival rate: {individual.survival_rate*100:.0f}%\n\n"
        
        return summary
    
    def random_mating(self) -> str:
        """Randomly pair individuals (no self-mating). Each pair produces 2 offspring."""
        self.generation += 1
        alive_individuals = [ind for ind in self.population.values() if ind.is_alive]
        
        if len(alive_individuals) < 2:
            return "❌ Need at least 2 alive individuals to mate!"
        
        random.shuffle(alive_individuals)
        pairs = []
        
        for i in range(0, len(alive_individuals) - 1, 2):
            pairs.append((alive_individuals[i], alive_individuals[i + 1]))
        
        unmated = alive_individuals[-1] if len(alive_individuals) % 2 == 1 else None
        
        offspring_count = 0
        new_offspring_ids = []
        
        for parent1, parent2 in pairs:
            for offspring_num in range(2):
                offspring_id = f"G{self.generation}_Offspring{offspring_count + 1}"
                offspring_genotypes = self._inherit_genotypes(parent1, parent2)
                offspring_phenotypes = self._calculate_phenotypes(offspring_genotypes)
                
                offspring = Individual(
                    id=offspring_id,
                    genotypes=offspring_genotypes,
                    phenotypes=offspring_phenotypes,
                    generation=self.generation,
                    parents=(parent1.id, parent2.id),
                    is_alive=True,
                    survival_rate=0.5
                )
                
                self.population[offspring_id] = offspring
                new_offspring_ids.append(offspring_id)
                offspring_count += 1
            
            self.mating_events.append(MatingEvent(
                parent1_id=parent1.id,
                parent2_id=parent2.id,
                offspring_ids=new_offspring_ids[-2:]
            ))
        
        report = (f"✓ **MATING PHASE COMPLETE**\n\n"
                 f"🔗 Mating pairs: {len(pairs)}\n"
                 f"👶 Offspring produced: {offspring_count}\n")
        
        if unmated:
            report += f"😔 Unmated (odd number): {unmated.id}\n"
        
        report += f"\n📈 New population size: {len(self.population)}\n"
        
        return report
    
    def _inherit_genotypes(self, parent1: Individual, parent2: Individual) -> Dict[str, Tuple[str, str]]:
        """Offspring inherit one allele from each parent for each trait."""
        offspring_genotypes = {}
        
        for trait in self.trait_definitions.keys():
            p1_allele1, p1_allele2 = parent1.genotypes[trait]
            p2_allele1, p2_allele2 = parent2.genotypes[trait]
            
            offspring_allele1 = random.choice([p1_allele1, p1_allele2])
            offspring_allele2 = random.choice([p2_allele1, p2_allele2])
            
            alleles = sorted([offspring_allele1, offspring_allele2],
                           key=lambda x: (x.lower(), x.islower()))
            
            offspring_genotypes[trait] = tuple(alleles)
        
        return offspring_genotypes
    
    def apply_beneficial_mutation(self) -> str:
        """Select one random offspring from F1 generation. Apply a beneficial mutation to one random trait."""
        f1_offspring = [ind for ind in self.population.values() 
                       if ind.generation == self.generation and ind.parents is not None]
        
        if not f1_offspring:
            return "❌ No F1 offspring to mutate!"
        
        mutant = random.choice(f1_offspring)
        trait_to_mutate = random.choice(list(self.trait_definitions.keys()))
        trait_def = self.trait_definitions[trait_to_mutate]
        
        old_allele1, old_allele2 = mutant.genotypes[trait_to_mutate]
        
        mutation_allele = f"{trait_to_mutate[0].upper()}*"
        
        if random.choice([True, False]):
            mutant.genotypes[trait_to_mutate] = (mutation_allele, old_allele2)
        else:
            mutant.genotypes[trait_to_mutate] = (old_allele1, mutation_allele)
        
        mutant.phenotypes = self._calculate_phenotypes(mutant.genotypes)
        mutant.has_mutation = True
        mutant.survival_rate = 0.75
        
        self.mutation_event = {
            'individual': mutant.id,
            'trait': trait_to_mutate,
            'old_genotype': f"{old_allele1}{old_allele2}",
            'new_genotype': f"{mutant.genotypes[trait_to_mutate][0]}{mutant.genotypes[trait_to_mutate][1]}",
            'new_phenotype': mutant.phenotypes[trait_to_mutate],
            'habitat': self.habitat,
            'survival_advantage': '75% vs 50%'
        }
        
        return (f"🧬 **BENEFICIAL MUTATION APPLIED**\n\n"
                f"Individual: **{mutant.id}**\n"
                f"Trait mutated: **{trait_to_mutate}**\n"
                f"Old genotype: {old_allele1}{old_allele2}\n"
                f"New genotype: {mutant.genotypes[trait_to_mutate][0]}{mutant.genotypes[trait_to_mutate][1]}\n"
                f"New phenotype: {mutant.phenotypes[trait_to_mutate]}\n\n"
                f"💪 Survival advantage: **75%** (vs 50% for normal individuals)\n"
                f"🏠 Why beneficial: This trait helps in **{self.habitat}** habitat!")
    
    def apply_survival_filtering(self) -> str:
        """All individuals survive independently. Normal: 50%, Mutant: 75%."""
        self.survival_records = []
        
        survived_count = 0
        died_count = 0
        
        for individual in self.population.values():
            if individual.has_mutation:
                survival_chance = 0.75
            else:
                survival_chance = 0.50
            
            random_roll = random.random()
            dies = random_roll > survival_chance
            
            if dies:
                individual.is_alive = False
                died_count += 1
                status = "❌ DIED"
            else:
                survived_count += 1
                status = "✅ SURVIVED"
            
            self.survival_records.append({
                'individual': individual.id,
                'survival_rate': survival_chance,
                'status': status,
                'generation': individual.generation,
                'has_mutation': individual.has_mutation
            })
        
        self.population_history[self.generation] = survived_count
        
        report = (f"⚔️ **SURVIVAL FILTERING COMPLETE**\n\n"
                 f"Survived: **{survived_count}**\n"
                 f"Died: **{died_count}**\n"
                 f"Population after survival: **{survived_count}**\n\n"
                 f"Survival rates applied:\n"
                 f"  • Normal individuals: 50%\n"
                 f"  • Mutant individual: 75%\n\n"
                 f"💡 Note: Survival is **probabilistic**, not guaranteed!\n"
                 f"Even beneficial traits can be lost by chance.")
        
        return report
