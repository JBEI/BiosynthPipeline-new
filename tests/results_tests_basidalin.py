from biosynth_pipeline import biosynth_pipeline
from rdkit import Chem
import warnings

warnings.simplefilter('ignore')

def test_basidalin():
    ### User-defined parameters
    pathway_sequence = ['pks', 'bio']  # choose between ['pks'] or ['pks','bio']
    target_smiles = 'NC1=CC(=CCO)OC1N'
    target_name = 'basidalin'
    pks_release_mechanism = 'cyclization' # choose from 'cyclization' or 'thiolysis'
    feasibility_cofactors = '../data/coreactants_and_rules/all_cofactors_updated.csv'

    ### Create an object that is an instance of the feasibility classification model
    PX = biosynth_pipeline.feasibility_classifier(ML_model_type = 'add_concat',
                                                  cofactors_path = feasibility_cofactors)

    ### Create an object that is an instance of Biosynth Pipeline
    biosynth_pipeline_object = biosynth_pipeline.biosynth_pipeline(
                                                 pathway_sequence = pathway_sequence,
                                                 target_smiles = target_smiles,
                                                 target_name = target_name,
                                                 feasibility_classifier = PX,
                                                 pks_release_mechanism = pks_release_mechanism,
                                                 config_filepath = f'{target_name}_input_config.json')

    biosynth_pipeline_object.run_combined_synthesis(max_designs = 4)
    biosynth_pipeline_object.save_results_logs()

    with open(f'./test_molecules/{target_name}_results/{target_name}_{pathway_sequence[0].capitalize()}_'
              f'{pathway_sequence[1].capitalize()}2.txt', 'r') as file:
        mol = Chem.MolFromSmiles(target_smiles)
        canonical_smiles = Chem.MolToSmiles(mol)

        counter = 0
        for line in file:
            if 'product similarity: 1.0' in line or f'product: {canonical_smiles}' in line:
                counter +=1

        assert counter >= 1

test_basidalin()