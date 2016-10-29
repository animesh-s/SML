from diff_match_patch import diff_match_patch

def diff_inserted_text(old_text, new_text):
    diff_object = diff_match_patch()
    diff = diff_object.diff_main(old_text, new_text)
    additions = [item[1] for item in diff if item[0] == 1]
    inserted_text = "".join(additions)
    inserted_text = inserted_text.replace(" ", "")
    return inserted_text
