# Install required package if not already installed:
# pip install sentence-transformers torch

from sentence_transformers import SentenceTransformer, util

# Load Sentence-BERT model once (fast and robust)
fast_model = SentenceTransformer("all-MiniLM-L6-v2")

def fast_score_teacher(question, student_answer, reference_answer, max_marks=2):
    """
    Fast scoring similar to teacher grading:
    - High similarity → full marks
    - Medium similarity → partial marks
    - Low similarity → no marks
    
    Args:
        question (str): Rubric question (optional for context)
        student_answer (str): Student's answer
        reference_answer (str): Correct/reference answer
        max_marks (float): Maximum marks for the question

    Returns:
        score (float): Marks awarded
        similarity (float): Cosine similarity between student and reference
    """
    # Encode embeddings
    sa_emb = fast_model.encode(student_answer, convert_to_tensor=True)
    ra_emb = fast_model.encode(reference_answer, convert_to_tensor=True)

    # Compute semantic similarity
    sim = util.cos_sim(sa_emb, ra_emb).item()

    # Teacher-like marks thresholds
    if sim >= 0.85:
        score = max_marks          # Full marks
    elif sim >= 0.65:
        score = max_marks * 0.75   # 3/4 marks
    elif sim >= 0.5:
        score = max_marks * 0.5    # Half marks
    else:
        score = 0.0                # No marks

    return score, sim

# -------------------------------
# Example Usage
# -------------------------------

if __name__ == "__main__":
    question = "Explain photosynthesis"
    
    # Example student answers
    student_answers = [
        "Photosynthesis is the process by which plants make food using sunlight.",  # almost correct
        "It converts light into chemical energy in plants.",                         # partial
        "Plants eat sunlight.",                                                      # wrong
    ]
    
    reference_answer = "Photosynthesis is the process where plants convert sunlight into chemical energy to produce food."

    max_marks = 3

    for idx, ans in enumerate(student_answers, 1):
        score, similarity = fast_score_teacher(question, ans, reference_answer, max_marks=max_marks)
        print(f"Student Answer {idx}: {ans}")
        print(f" → Similarity: {round(similarity,3)}, Marks Awarded: {round(score,2)}\n")
