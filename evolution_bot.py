import random
from typing import List, Dict, Tuple
from collections import Counter
from dataclasses import dataclass, field

@dataclass
class Individual:
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
    parent1_id: str
    parent2_id: str
    offspring_ids: List[str]

class EvolutionSimulationBot:
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
        self.habitat = habitat.strip()
        return f"Habitat set: {self.habitat}"
    
    def define_trait(self, trait_name: str, dominant_allele: str, recessive_allele: str, dominant_phenotype: str, recessive_phenotype: str) -> str:
        self.trait_definitions[trait_name] = {
            'dominant_allele': dominant_allele.upper(),
            'recessive_allele': recessive_allele.lower(),
            'dominant_phenotype': dominant_phenotype,
            'recessive_phenotype': recessive_phenotype
        }
        return f"Trait defined: {trait_name}"
    
    def add_individual(self, individual_id: str, genotypes: Dict[str, Tuple[str, str]]) -> str:
        for trait, (allele1, allele2) in genotypes.items():
            if trait not in self.trait_definitions:
                return f"Error: Trait '{trait}' not defined!"
        
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
        return f"Added {individual_id}"
    
    def _calculate_phenotypes(self, genotypes: Dict[str, Tuple[str, str]]) -> Dict[str, str]:
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
        if not self.population:
            return "Population is empty!"
        summary = f"\nGeneration {self.generation}\n"
        summary += f"Total: {len(self.population)}\n"
        summary += f"Alive: {sum(1 for ind in self.population.values() if ind.is_alive)}\n\n"
        for ind_id, individual in sorted(self.population.items()):
            status = "ALIVE" if individual.is_alive else "DEAD"
            summary += f"{ind_id} ({status})\n"
            for trait, (allele1, allele2) in individual.genotypes.items():
                phenotype = individual.phenotypes[trait]
                summary += f"  {trait}: {allele1}{allele2} -> {phenotype}\n"
        return summary
    
    def random_mating(self) -> str:
        self.generation += 1
        alive_individuals = [ind for ind in self.population.values() if ind.is_alive]
        if len(alive_individuals) < 2:
            return "Need at least 2 alive individuals to mate!"
        
        random.shuffle(alive_individuals)
        pairs = []
        for i in range(0, len(alive_individuals) - 1, 2):
            pairs.append((alive_individuals[i], alive_individuals[i + 1]))
        
        offspring_count = 0
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
                offspring_count += 1
            self.mating_events.append(MatingEvent(
                parent1_id=parent1.id,
                parent2_id=parent2.id,
                offspring_ids=[f"G{self.generation}_Offspring{offspring_count - 1}", f"G{self.generation}_Offspring{offspring_count}"]
            ))
        
        return f"Mating complete: {len(pairs)} pairs, {offspring_count} offspring"
    
    def _inherit_genotypes(self, parent1: Individual, parent2: Individual) -> Dict[str, Tuple[str, str]]:
        offspring_genotypes = {}
        for trait in self.trait_definitions.keys():
            p1_allele1, p1_allele2 = parent1.genotypes[trait]
            p2_allele1, p2_allele2 = parent2.genotypes[trait]
            offspring_allele1 = random.choice([p1_allele1, p1_allele2])
            offspring_allele2 = random.choice([p2_allele1, p2_allele2])
            alleles = sorted([offspring_allele1, offspring_allele2], key=lambda x: (x.lower(), x.islower()))
            offspring_genotypes[trait] = tuple(alleles)
        return offspring_genotypes
        def apply_custom_mutation(self, individual_id: str, trait: str, new_allele: str) -> str:
        """Apply a custom mutation to a specific individual in a specific generation."""
        if individual_id not in self.population:
            return f"Error: Individual {individual_id} not found!"
        
        if trait not in self.trait_definitions:
            return f"Error: Trait {trait} not defined!"
        
        mutant = self.population[individual_id]
        old_allele1, old_allele2 = mutant.genotypes[trait]
        
        if random.choice([True, False]):
            mutant.genotypes[trait] = (new_allele, old_allele2)
        else:
            mutant.genotypes[trait] = (old_allele1, new_allele)
        
        mutant.phenotypes = self._calculate_phenotypes(mutant.genotypes)
        mutant.has_mutation = True
        mutant.survival_rate = 0.75
        
        self.mutation_event = {
            'individual': mutant.id,
            'trait': trait,
            'old_genotype': f"{old_allele1}{old_allele2}",
            'new_genotype': f"{mutant.genotypes[trait][0]}{mutant.genotypes[trait][1]}",
            'habitat': self.habitat
        }
        
        return f"Custom mutation applied to {individual_id}: {trait} mutation to {new_allele}"

    def apply_beneficial_mutation(self) -> str:
        f1_offspring = [ind for ind in self.population.values() if ind.generation == self.generation and ind.parents is not None]
        if not f1_offspring:
            return "No F1 offspring to mutate!"
        
        mutant = random.choice(f1_offspring)
        trait_to_mutate = random.choice(list(self.trait_definitions.keys()))
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
            'habitat': self.habitat
        }
        
        return f"Mutation applied to {mutant.id}: {trait_to_mutate}"
    
    def apply_survival_filtering(self) -> str:
        self.survival_records = []
        survived_count = 0
        died_count = 0
        
        for individual in self.population.values():
            survival_chance = 0.75 if individual.has_mutation else 0.50
            random_roll = random.random()
            dies = random_roll > survival_chance
            
            if dies:
                individual.is_alive = False
                died_count += 1
            else:
                survived_count += 1
            
            self.survival_records.append({
                'individual': individual.id,
                'survival_rate': survival_chance,
                'alive': individual.is_alive
            })
        
        self.population_history[self.generation] = survived_count
        return f"Survival filtering: {survived_count} survived, {died_count} died"

