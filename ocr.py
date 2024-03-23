import cv2
import pytesseract
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
# import matplotlib.pyplot as plt
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import words
from nltk.corpus import stopwords
from nltk import download
from nltk import WordNetLemmatizer, pos_tag
from nltk.corpus import wordnet
from spellchecker import SpellChecker

download('punkt')
download('words')
download('stopwords')
download('wordnet')

spell_checker = SpellChecker()

def postprocess_text(text):
    # Tokenisation des mots
    tokens = word_tokenize(text)
    
    # Correction orthographique
    corrected_tokens = []
    for token in tokens:
        if token.lower() not in words.words():
            corrected_token = spell_checker.correction(token)
            if corrected_token is not None:  # Vérifier si la correction n'est pas None
                corrected_tokens.append(corrected_token)
        else:
            corrected_tokens.append(token)
    
    # Reconstruction du texte corrigé
    corrected_text = ' '.join(corrected_tokens)
    
    return corrected_text


# Définition de la fonction pour supprimer l'arrière-plan de l'image
# def remove_background(image):
#     # Convertir l'image en niveaux de gris
#     gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
#     # Appliquer un flou gaussien pour réduire le bruit
#     blurred = cv2.GaussianBlur(gray, (15, 15), 0)  # Ajuster la taille du noyau au besoin
    
#     # Appliquer la méthode de soustraction de l'arrière-plan avec un seuil adapté
#     _, thresh = cv2.threshold(blurred, 200, 255, cv2.THRESH_BINARY)  # Ajuster le seuil au besoin
    
#     # Appliquer des opérations morphologiques pour améliorer la qualité du masque
#     fgmask = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (15, 15)))  # Utiliser MORPH_CLOSE pour remplir les petits trous
    
#     # Appliquer le masque sur l'image originale
#     result = cv2.bitwise_and(image, image, mask=fgmask)
    
#     return result


# Fonction principale pour effectuer l'OCR à partir d'un fichier
def ocr_from_file(remove_bg=False):
    filepath = filedialog.askopenfilename(title="Sélectionner une image",
                                           filetypes=[("Fichiers image", "*.jpg;*.jpeg;*.png;*.bmp")])
    if filepath:
        img = cv2.imread(filepath)
        if img is not None:
            cv2.imshow("Image originale", img)
            cv2.waitKey(0)
            cv2.destroyAllWindows()
            
            if remove_bg:
                img_processed = remove_background(img)
                cv2.imshow("Image après traitement", img_processed)
                cv2.waitKey(0)
                cv2.destroyAllWindows()

                img = img_processed
            
            # Extraction du texte
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            _, binary = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
            blurred = cv2.GaussianBlur(binary, (3, 3), 0)
            text = pytesseract.image_to_string(blurred)
            
            # Post-traitement du texte
            corrected_text = postprocess_text(text)
            
            # Affichage du texte extrait
            messagebox.showinfo("Texte extrait", corrected_text)
            
        else:
            messagebox.showerror("Erreur", "Impossible de charger l'image.")
    else:
        messagebox.showinfo("Info", "Aucun fichier sélectionné.")
# Fonction principale
def main():
    root = tk.Tk()
    root.title("OCR Application")

    # Définir la variable globale pour le bouton remove_bg_checkbox
    global remove_bg_var
    remove_bg_var = tk.BooleanVar()

    # Créer le bouton pour supprimer l'arrière-plan de l'image
    # remove_bg_checkbox = tk.Checkbutton(root, text="Supprimer l'arrière-plan de l'image", variable=remove_bg_var)
    # remove_bg_checkbox.pack(pady=10)

    # Créer le bouton pour sélectionner une image et lancer l'OCR
    button = tk.Button(root, text="Sélectionner une image", command=lambda: ocr_from_file(remove_bg=remove_bg_var.get()))
    button.pack(pady=20)

    root.mainloop()

if __name__ == "__main__":
    main()
