# def post_process_freq(labels):
#     grouped = {
#         'make': [],
#         'model': [],
#         'variant': [],
#         'overall_name': []
#     }

#     for img, predictions in labels.items():
#         for conf, class_name in predictions:
#             if re.search(r'_logo$|_badge$', class_name):
#                 grouped['make'].append((conf, class_name.split("_")[0]))
#             elif class_name.endswith("_model"):
#                 grouped['model'].append((conf, class_name.split("_")[0]))
#             elif class_name.endswith("_variant"):
#                 grouped['variant'].append((conf, class_name.split("_")[0]))
#             elif re.search(r'\d{4}-\d{4}', class_name):
#                 grouped['overall_name'].append((conf, class_name))

#     if grouped['variant']:
#         unique_variants = list(set([label for _, label in grouped['variant']]))
#         if len(unique_variants) > 1:
#             variant_prefixes = [v.split("_")[0] for v in unique_variants]
#             merged_variant = "-".join(set(variant_prefixes)) + "_variant"
#             grouped['variant'] = [(1.0, merged_variant)]
#         else:
#             grouped['variant'] = [(conf, label) for conf, label in grouped['variant']]

#     frequencies = {}
#     for group, items in grouped.items():
#         freq_counter = Counter()
#         conf_counter = defaultdict(float)

#         for conf, label in items:
#             freq_counter[label] += 1
#             conf_counter[label] += conf

#         frequencies[group] = sorted(
#             [(label, freq_counter[label], conf_counter[label] / freq_counter[label])
#              for label in freq_counter],
#             key=lambda x: (x[1], x[2]),
#             reverse=True
#         )
#     return frequencies


# def final_labels(freq):
#     m1 = m2 = v = y = "Unknown"
#     if freq['make']:
#         m1 = freq['make'][0][0].split("_")[0]
#     if freq['model']:
#         m2 = freq['model'][0][0].split("_")[0]
#     if freq['variant']:
#         v = freq['variant'][0][0].split("_")[0]
#     for label, _, _ in freq['overall_name']:
#         split_label = label.split("_")
#         if len(split_label) == 4:
#             make, model, variant, year_range = split_label
#             if make == m1 and model == m2 and variant == v:
#                 y = year_range
#                 break
#     return m1, m2, v, y


# def check_consistency(freq):
#     conflicts = {}
#     for key in ['make', 'model', 'variant', 'overall_name']:
#         if len(freq[key]) > 1:
#             conflicts[key] = [item[0] for item in freq[key]]
#     return conflicts

