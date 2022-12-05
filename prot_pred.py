import streamlit as st
from stmol import showmol
import py3Dmol
import requests
import biotite.structure.io as bsio

st.sidebar.title("Protein Structure Predictor")
st.sidebar.write(
    '[*ESMFold*](https://esmatlas.com/about) is an end-to-end single sequence protein structure predictor based on the ESM-2 language model. For more information, read the [research article](https://www.biorxiv.org/content/10.1101/2022.07.20.500902v2) and the [news article](https://www.nature.com/articles/d41586-022-03539-1) published in *Nature*.')
st.sidebar.write('Created by: Souradipto Choudhuri')


def render_mol(pdb):
    pdbview = py3Dmol.view()
    pdbview.addModel(pdb, 'pdb')
    pdbview.setStyle({'cartoon': {'color': 'spectrum', 'arrows': True}})
    # pdbview.setStyle({'stick': {'colorscheme': 'ssPyMOL'}})
    pdbview.setBackgroundColor('white')
    pdbview.zoomTo()
    pdbview.zoom(2, 800)
    pdbview.spin(True)
    showmol(pdbview, height=950, width=1000)


df_prot_seq = 'AIEEGKLVIWINGDKGYNGLAEVGKKFEKDTGIKVTVEHPDKLEEKFPQVAATGDGPDIIFWAHDRFGGYAQSGLLAEITPDKAFQDKLYPFTWDAVRYNGKLIAYPIAVEALSLIYNKDLLPNPPKTWEEIPALDKELKAKGKSALMFNLQEPYFTWPLIAADGGYAFKYENGKYDIKDVGVDNAGAKAGLTFLVDLIKNKHMNADTDYSIAEAAFNKGETAMTINGPWAWSNIDTSKVNYGVTVLPTFKGQPSKPFVGVLSAGINAASPNKELAKEFLENYLLTDEGLEAVNKDKPLGAVALKSYEEELAKDPRIAATMENAQKGEIMPNIPQMSAFWYAVRTAVINAASGRQTVDEALKDAQTRITK'
txt = st.sidebar.text_area('Input Sequence', df_prot_seq, height=275)


def update(seq=txt):
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
    }
    response = requests.post('https://api.esmatlas.com/foldSequence/v1/pdb/', headers=headers, data=seq)
    name = seq[:3] + seq[-3:]
    pdb_str = response.content.decode('utf-8')

    with open('predicted.pdb', 'w') as out_file:
        out_file.write(pdb_str)

    struct = bsio.load_structure('predicted.pdb', extra_fields=['b_factor'])
    b_val = round(struct.b_factor.mean(), 4)

    # Display the struct
    st.subheader('Predicted model')
    render_mol(pdb_str)

    # Calculating the plDDT val
    st.subheader('plDDT Value')
    st.write('plDDT is a per-residue estimate of the confidence in prediction on a scale from 0-100.')
    st.info(f'plDDT: {b_val}')

    st.download_button(
        label='Download PDB',
        data=pdb_str,
        file_name='Predicted.pdb',
        mime='text/plain'
    )


predict = st.sidebar.button('Predict', on_click=update)

if not predict:
    st.warning('Enter Protein Sequence Data')
