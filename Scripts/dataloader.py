import json
import os

def load_json(filepath):
    with open(filepath, 'r') as f:
        return json.load(f)

# counterfact
def process_counterfact_dataset(filepath, transformed_data):
    counterfact_data = load_json(filepath)
    for item in counterfact_data:
        case_id = item['case_id']
        pararel_idx = item['pararel_idx']
        requested_rewrite = item['requested_rewrite']
        subject = requested_rewrite['subject']
        original_answer = requested_rewrite['target_true']['str']
        edited_answer = requested_rewrite['target_new']['str']

        for query in item['paraphrase_prompts']:
            transformed_data.append({
                'Dataset': 'Counterfact',
                'Edit': requested_rewrite['prompt'],
                'subject': subject,
                'original_answer': original_answer,
                'edited_answer': edited_answer,
                'query_type': 'paraphrase',
                'query': query,
                'correct_answer': edited_answer,
                'incorrect_answer': original_answer,
                'condition_type': None
            })

        for query in item['neighborhood_prompts']:
            transformed_data.append({
                'Dataset': 'Counterfact',
                'Edit': requested_rewrite['prompt'],
                'subject': subject,
                'original_answer': original_answer,
                'edited_answer': edited_answer,
                'query_type': 'neighborhood',
                'query': query,
                'correct_answer': original_answer,
                'incorrect_answer': edited_answer,
                'condition_type': None
            })

        for query in item['attribute_prompts']:
            transformed_data.append({
                'Dataset': 'Counterfact',
                'Edit': requested_rewrite['prompt'],
                'subject': subject,
                'original_answer': original_answer,
                'edited_answer': edited_answer,
                'query_type': 'attribute',
                'query': query,
                'correct_answer': edited_answer,
                'incorrect_answer': original_answer,
                'condition_type': None
            })

# rippleedits
def process_rippleedits_dataset(filepath, transformed_data):
    rippleedits_data = load_json(filepath)
    
    def process_rippleedits_queries(data, dataset_name, condition_type=None):
        for item in data:
            if isinstance(item, dict):
                for section_name, section_data in item.items():
                    if isinstance(section_data, list):
                        for query_item in section_data:
                            for query in query_item.get('test_queries', []):
                                for answer in query['answers']:
                                    transformed_data.append({
                                        'Dataset': dataset_name,
                                        'Edit': query['prompt'],
                                        'subject': query['subject_id'],
                                        'original_answer': None,
                                        'edited_answer': answer['value'],
                                        'query_type': query['query_type'],
                                        'query': query['prompt'],
                                        'correct_answer': answer['value'],
                                        'incorrect_answer': None,
                                        'condition_type': condition_type
                                    })
                            for condition_query in query_item.get('condition_queries', []):
                                for answer in condition_query['answers']:
                                    transformed_data.append({
                                        'Dataset': dataset_name,
                                        'Edit': condition_query['prompt'],
                                        'subject': condition_query['subject_id'],
                                        'original_answer': None,
                                        'edited_answer': answer['value'],
                                        'query_type': condition_query['query_type'],
                                        'query': condition_query['prompt'],
                                        'correct_answer': answer['value'],
                                        'incorrect_answer': None,
                                        'condition_type': 'condition'
                                    })

    process_rippleedits_queries(rippleedits_data, 'RippleEdits')

# mquake
def process_mquake_dataset(filepath, transformed_data):
    mquake_data = load_json(filepath)
    for item in mquake_data:
        case_id = item['case_id']
        for rewrite in item['requested_rewrite']:
            subject = rewrite['subject']
            original_answer = rewrite['target_true']['str']
            edited_answer = rewrite['target_new']['str']
            prompt = rewrite['prompt']

            for query in item['questions']:
                transformed_data.append({
                    'Dataset': 'MQuAKE',
                    'Edit': prompt,
                    'subject': subject,
                    'original_answer': original_answer,
                    'edited_answer': edited_answer,
                    'query_type': 'question',
                    'query': query,
                    'correct_answer': original_answer,
                    'incorrect_answer': edited_answer,
                    'condition_type': None
                })

            for hop in item['single_hops']:
                for alias in hop['answer_alias']:
                    transformed_data.append({
                        'Dataset': 'MQuAKE',
                        'Edit': prompt,
                        'subject': subject,
                        'original_answer': original_answer,
                        'edited_answer': edited_answer,
                        'query_type': 'single_hop',
                        'query': hop['question'],
                        'correct_answer': hop['answer'],
                        'incorrect_answer': alias,
                        'condition_type': None
                    })

            for new_hop in item['new_single_hops']:
                for alias in new_hop['answer_alias']:
                    transformed_data.append({
                        'Dataset': 'MQuAKE',
                        'Edit': prompt,
                        'subject': subject,
                        'original_answer': original_answer,
                        'edited_answer': edited_answer,
                        'query_type': 'new_single_hop',
                        'query': new_hop['question'],
                        'correct_answer': new_hop['answer'],
                        'incorrect_answer': alias,
                        'condition_type': None
                    })

# knowedit
# no idea how to properly write a function for this one as its a compilation of a bunch of different datasets
# placeholder
def process_knowedit_dataset(filepath, transformed_data):
    knowedit_data = load_json(filepath)
    for item in knowedit_data:
        transformed_data.append({
            'Dataset': 'KnowEdit',
            'Edit': item['template'],
            'subject': item['subject'],
            'original_answer': None,
            'edited_answer': item['attribute'],
            'query_type': 'rake',
            'query': item['prompt'],
            'correct_answer': item['attribute'],
            'incorrect_answer': item['prediction'],
            'condition_type': None
        })

# rake
def process_rake_dataset(filepath, transformed_data):
    

    rake_data = load_json(filepath)
    for item in rake_data:
        transformed_data.append({
            'Dataset': 'Rake',
            'Edit': item['template'],
            'subject': item['subject'],
            'original_answer': None,
            'edited_answer': item['attribute'],
            'query_type': 'rake',
            'query': item['prompt'],
            'correct_answer': item['attribute'],
            'incorrect_answer': item['prediction'],
            'condition_type': None
        })

# pep3k-20qa
def process_pep3k20qa_dataset(filepath, transformed_data):
    pep3k20qa_data = load_json(filepath)
    # placeholder
    pass

# TAXI
def process_edits_evaluation_dataset(filepath, transformed_data):
    edits_evaluation_data = load_json(filepath)
    for item in edits_evaluation_data:
        transformed_data.append({
            'Dataset': 'edits-evaluation',
            'Edit': item['template'],
            'subject': item['subject'],
            'original_answer': item['attribute'],
            'edited_answer': item['prediction'],
            'query_type': 'evaluation',
            'query': item['prompt'],
            'correct_answer': item['attribute'],
            'incorrect_answer': item['prediction'],
            'condition_type': None
        })

def load_data(dataset):
    transformed_data = []
    dataset_paths = {
            "counterfact": "counterfact\\Counterfact.json",
            "rippledits": "RippleEdits\\popular.json",
            "mquake": "MQuAKE\\MQuAKE-T.json",
            # "knowedit": KnowEditDataset('the_json_path'),
            "rake": "Editbench Project\\known_1000.json",
            "pep3k-20qa": "pep3k-20qa.json",  # need to update
            "taxi": "TAXI\\edits-evaluation.json"
        }

    current_directory = os.getcwd()
    for key in dataset_paths:
        dataset_paths[key] = os.path.join(current_directory, dataset_paths[key])
       

    if dataset == "counterfact":
        process_counterfact_dataset(dataset_paths["counterfact"], transformed_data)

    elif dataset == "rippledits":
        process_rippleedits_dataset(dataset_paths["rippledits"], transformed_data)

    elif dataset == "mquake":
        process_mquake_dataset(dataset_paths["mquake"], transformed_data)

    elif dataset == "knowedit":
        process_knowedit_dataset(dataset_paths["knowedit"], transformed_data)

    elif dataset == "rake":
        process_rake_dataset(dataset_paths["rake"], transformed_data)

    elif dataset == "pep3k-20qa":
        process_pep3k20qa_dataset(dataset_paths["pep3k-20qa"], transformed_data)

    elif dataset == "taxi":
        process_edits_evaluation_dataset(dataset_paths["taxi"], transformed_data)

    else:
        raise ValueError(f"Unknown dataset: {dataset}")

    return transformed_data







