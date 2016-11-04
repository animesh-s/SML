python ../features/anonymous.py 
now=$(date +"%T")
echo "Anonymous Calculated $now"
python ../features/comment_length.py  
now=$(date +"%T")
echo "Comment Length Calculated $now"
python ../features/longest_word.py
now=$(date +"%T")
echo "Longest Word Calculated $now"
python ../features/size_increment.py
now=$(date +"%T")
echo "Size increment Calculated $now"
python ../features/ratios.py
now=$(date +"%T")
echo "Ratios Calculated $now"
python ../features/longest_character_sequence.py
now=$(date +"%T")
echo "Longest Character Sequence Calculated $now"
python ../features/character_distribution.py
now=$(date +"%T")
echo "Character Distribution Calculated $now"
python ../features/average_term_frequency.py
now=$(date +"%T")
echo "Average Term Frequency Calculated $now"
python ../features/character_diversity.py
now=$(date +"%T")
echo "Character Diversity Calculated $now"
python ../features/word_categories.py
now=$(date +"%T")
echo "Word Categories Calculated. Finished $now"
