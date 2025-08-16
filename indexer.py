\
import os
import zipfile
import glob
import pickle
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from .utils import clean_tamil_text, normalize_for_search

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")
INDEX_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "index")

TARGET_CSV = "Thirukural With Explanation.csv"

def _maybe_extract_csv_from_zip():
    """If a zip containing the target CSV exists in data/, extract it."""
    zips = glob.glob(os.path.join(DATA_DIR, "*.zip"))
    for zpath in zips:
        try:
            with zipfile.ZipFile(zpath) as zf:
                names = zf.namelist()
                matches = [n for n in names if n.lower().endswith(TARGET_CSV.lower()) or n.lower().endswith("thirukural with explanation.csv")]
                if matches:
                    zf.extract(matches[0], DATA_DIR)
                    # Move/rename to standard name
                    src = os.path.join(DATA_DIR, matches[0])
                    dst = os.path.join(DATA_DIR, TARGET_CSV)
                    if src != dst:
                        os.replace(src, dst)
                    return dst
        except zipfile.BadZipFile:
            pass
    return None

def load_dataset():
    """Load and clean the dataset; add a KuralNumber column (1..1330)."""
    csv_path = os.path.join(DATA_DIR, TARGET_CSV)
    if not os.path.exists(csv_path):
        _maybe_extract_csv_from_zip()
    if not os.path.exists(csv_path):
        raise FileNotFoundError(f"Could not find {TARGET_CSV} in {DATA_DIR}.")

    df = pd.read_csv(csv_path)
    # Expected columns: Chapter Name, Section Name, Verse, Translation, Explanation
    # Clean text columns
    for col in ["Chapter Name", "Section Name", "Verse", "Translation"]:
        if col in df.columns:
            df[col] = df[col].astype(str).map(clean_tamil_text)
    if "Explanation" in df.columns:
        df["Explanation"] = df["Explanation"].astype(str).map(clean_tamil_text)
    else:
        df["Explanation"] = ""

    # Add KuralNumber as 1..N
    df.insert(0, "KuralNumber", range(1, len(df) + 1))

    # Prepare a combined searchable text
    df["search_blob"] = (
        df["Verse"].map(normalize_for_search) + " | " +
        df["Translation"].map(normalize_for_search) + " | " +
        df["Explanation"].map(normalize_for_search) + " | " +
        df["Chapter Name"].map(normalize_for_search) + " | " +
        df["Section Name"].map(normalize_for_search)
    )
    return df

def build_index(force=False):
    os.makedirs(INDEX_DIR, exist_ok=True)
    index_path = os.path.join(INDEX_DIR, "tfidf.pkl")
    data_path = os.path.join(INDEX_DIR, "data.pkl")

    if not force and os.path.exists(index_path) and os.path.exists(data_path):
        return index_path, data_path

    df = load_dataset()

    vectorizer = TfidfVectorizer(min_df=1, max_df=0.95, ngram_range=(1,2))
    X = vectorizer.fit_transform(df["search_blob"].values.tolist())

    with open(index_path, "wb") as f:
        pickle.dump({"vectorizer": vectorizer, "matrix": X}, f)
    with open(data_path, "wb") as f:
        pickle.dump(df, f)

    return index_path, data_path

def load_index():
    index_path = os.path.join(INDEX_DIR, "tfidf.pkl")
    data_path = os.path.join(INDEX_DIR, "data.pkl")
    if not (os.path.exists(index_path) and os.path.exists(data_path)):
        build_index(force=True)
    with open(index_path, "rb") as f:
        idx = pickle.load(f)
    with open(data_path, "rb") as f:
        df = pickle.load(f)
    return idx["vectorizer"], idx["matrix"], df
