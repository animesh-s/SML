def calculate_metrics(true_positive, true_negative, false_positive, false_negative):
    total_sample = true_positive + true_negative + false_positive + false_negative
    accuracy = ((float)(true_positive + true_negative) / (total_sample)) * 100
    precision = ((float)(true_positive) / (true_positive + false_positive)) * 100
    recall = ((float)(true_positive) / (true_positive + false_negative)) * 100
    return accuracy, precision, recall