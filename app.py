import random
import streamlit as st

# ==========================================
# SAYFA YAPILANDIRMASI VE TEMA
# ==========================================
st.set_page_config(
    page_title="Latince Botanik Terminoloji Macerası",
    page_icon="🌿",
    layout="centered",
)

# ==========================================
# SESSION STATE (OTURUM DURUMU) BAŞLANGICI
# ==========================================
if "game_stage" not in st.session_state:
  st.session_state.game_stage = (
      "setup"  # setup, hub, etymology, diagnosis, expedition
  )
  st.session_state.botanist_name = ""
  st.session_state.specialization = ""
  st.session_state.knowledge_points = 50
  st.session_state.inventory = []

# ==========================================
# AŞAMA 1: BÖLÜM VE UZMANLIK SEÇİMİ (KAYIT)
# ==========================================
if st.session_state.game_stage == "setup":
  st.title("🌱 Botanik Bahçesine Hoş Geldiniz!")
  st.markdown(
      "### 🔬 Latince Botanik Terimleri ve Taksonomi Dünyasına Adım Atın!"
  )
  st.write(
      "Kraliyet Botanik Enstitüsü'ne hoş geldiniz. Bitkilerin bilimsel"
      " adlarını çözmek ve bir 'Usta Botanist' olmak için önce kaydınızı"
      " yapmalıyız."
  )

  with st.form("botanist_form"):
    name_input = st.text_input(
        "Botanist Adınız:", placeholder="Örn: Linnaeus"
    )

    st.markdown("### Uzmanlık Alanınızı Seçin:")
    specialization_choice = st.radio(
        "Hangi alanda uzmanlaşmak istiyorsunuz?",
        [
            "🌿 Taksatonomi & Bitki Adlandırma (Nomenclature)",
            "🌺 Morfoloji & Yapısal Özellikler (Morphology)",
            "💊 Etnobotanik & Tıbbi Bitkiler (Medicinalis)",
            "🌳 Ekoloji & Habitat (Ecology)",
        ],
    )

    submit_button = st.form_submit_button("Laboratuvara Giriş Yap!")

    if submit_button:
      if name_input.strip() == "":
        st.warning("Lütfen başlamak için adınızı girin!")
      else:
        st.session_state.botanist_name = name_input

        # Uzmanlığa göre etiket atama
        if "Taksatonomi" in specialization_choice:
          st.session_state.specialization = "Taksonom"
        elif "Morfoloji" in specialization_choice:
          st.session_state.specialization = "Morfolog"
        elif "Etnobotanik" in specialization_choice:
          st.session_state.specialization = "Etnobotanist"
        else:
          st.session_state.specialization = "Ekolog"

        st.success(
            f"Tebrikler **{st.session_state.botanist_name}**! Artık bir"
            f" **{st.session_state.specialization}** adayısınız."
        )
        st.balloons()
        st.session_state.game_stage = "hub"
        st.rerun()

# ==========================================
# AŞAMA 2: SERA MERKEZİ VE KONTROL PANELİ (HUB)
# ==========================================
elif st.session_state.game_stage == "hub":
  st.title(f"🪴 Ana Sera Merkezi, Dr. {st.session_state.botanist_name}")

  # Kenar Çubuğu (Sidebar) İstatistikleri
  st.sidebar.header("📋 Botanist Kartı")
  st.sidebar.write(f"**İsim:** {st.session_state.botanist_name}")
  st.sidebar.write(f"**Alan:** {st.session_state.specialization}")
  st.sidebar.metric(
      label="🧠 Bilgi Puanı", value=st.session_state.knowledge_points
  )
  st.sidebar.write(
      f"**Toplanan Örnekler:** {', '.join(st.session_state.inventory) if st.session_state.inventory else 'Henüz yok'}"
  )

  if st.sidebar.button("Oyunu Sıfırla 🔄"):
    st.session_state.clear()
    st.rerun()

  st.markdown("### Bugün Hangi Bölümü Araştırmak İstersiniz?")

  col1, col2, col3 = st.columns(3)

  with col1:
    if st.button("🧪 Etimoloji Lab"):
      st.session_state.game_stage = "etymology"
      st.rerun()

  with col2:
    if st.button("🔍 Örnek Teşhisi"):
      st.session_state.game_stage = "diagnosis"
      st.rerun()

  with col3:
    if st.button("🌳 Morfoloji Çölü"):
      st.session_state.game_stage = "expedition"
      st.rerun()

  # Oyun bitti mi kontrolü
  if st.session_state.knowledge_points <= 0:
    st.error(
        "Dikkat! Bilgi puanınız tükendi. Enstitü başkanı laboratuvarı"
        " kapatmanızı istiyor."
    )
    if st.button("Yeniden Dene 🔄"):
      st.session_state.knowledge_points = 50
      st.rerun()

# ==========================================
# AŞAMA 3A: ETİMOLOJİ LAB (KÖK VE ANLAM TESTİ)
# ==========================================
elif st.session_state.game_stage == "etymology":
  st.header("🧪 Latince Kökler ve Anlamlar Laboratuvarı")
  st.write(
      "Prof. Smith sana latince bir terim kökü uzatıyor: *'officinalis'*."
      " Bu terim botanik adlarda ne anlama gelir?"
  )

  meaning = st.selectbox(
      "Doğru anlamı seçin:",
      [
          "Seçiminizi yapın...",
          "Tıbbi / Eczacılıkta kullanılan (Medicinal)",
          "Kırmızı renkli yapraklara sahip",
          "Zehirli ve tehlikeli bitki",
      ],
  )

  if st.button("Cevabı Kontrol Et"):
    if "Tıbbi / Eczacılıkta" in meaning:
      st.success(
          "🎉 Harika! Doğru bildin. *Officinalis*, eczane/tıbbi geçmişi"
          " simgeler. +25 Bilgi Puanı!"
      )
      st.session_state.knowledge_points += 25
      st.session_state.inventory.append("Officinalis Örneği")
    elif "Seçiminizi" in meaning:
      st.warning("Lütfen bir seçenek seçin!")
    else:
      st.error("❌ Yanlış! Bu kök tıbbi bitkileri ifade eder. -15 Puan.")
      st.session_state.knowledge_points -= 15

  if st.button("🔙 Ana Seraya Dön"):
    st.session_state.game_stage = "hub"
    st.rerun()

# ==========================================
# AŞAMA 3B: BİNOMİAL ADLANDIRMA (ÖRNEK TEŞHİSİ)
# ==========================================
elif st.session_state.game_stage == "diagnosis":
  st.header("🔍 İkili Adlandırma (Binomial Nomenclature) Teşhisi")
  st.write(
      "Masada bir bitki var. Tür adı *sempervirens* (örn: *Cupressus"
      " sempervirens*)."
  )
  st.info("Soru: Bu bitkinin mevsimsel dövüşü/özelliği nedir?")

  property_choice = st.selectbox(
      "Bitkinin en belirgin özelliği nedir?",
      [
          "Seçiminizi yapın...",
          "Her dem yeşil (yaprak dökmez)",
          "Sadece kışın çiçek açar",
          "Tek yıllık otsu bitki",
      ],
  )

  if st.button("Teşhisi Tamamla"):
    if "Her dem yeşil" in property_choice:
      st.success(
          "✨ Doğru! *Semper* (daima) + *virens* (yeşil) = Her dem yeşil"
          " demektir. +30 Bilgi Puanı!"
      )
      st.session_state.knowledge_points += 30
      st.session_state.inventory.append("Sempervirens Örneği")
    elif "Seçiminizi" in property_choice:
      st.warning("Lütfen bir özellik seçin!")
    else:
      st.error("❌ Yanlış teşhis! Bitki yapraklarını dökmez. -15 Puan.")
      st.session_state.knowledge_points -= 15

  if st.button("🔙 Ana Seraya Dön"):
    st.session_state.game_stage = "hub"
    st.rerun()

# ==========================================
# AŞAMA 3C: MORFOLOJİ BİLMECESİ (YAPRAK VE ŞEKİL)
# ==========================================
elif st.session_state.game_stage == "expedition":
  st.header("🌳 Morfoloji Bilmece İstasyonu")
  st.write(
      "Eski bir botanik el yazmasında şu tanım yer alıyor: *'Mızrak şeklinde,"
      " uç kısmı sivri yaprak yapısı.'*"
  )

  term_input = st.text_input(
      "Bu morfolojik Latince terimi girin (İpucu: l...):",
      placeholder="Örn: lanceolatus",
  )

  if st.button("Gönder"):
    if term_input.strip().lower() in ["lanceolatus", "lanceolate"]:
      st.success(
          "📖 Mükemmel! *Lanceolatus* (mızrak biçimli) doğru cevap! +20 Bilgi"
          " Puanı."
      )
      st.session_state.knowledge_points += 20
      st.session_state.inventory.append("Lanceolatus Kartı")
    else:
      st.error(
          "❌ Yanlış terim! Doğru terim 'lanceolatus' olmalıydı. -10 Puan."
      )
      st.session_state.knowledge_points -= 10

  if st.button("🔙 Ana Seraya Dön"):
    st.session_state.game_stage = "hub"
    st.rerun()
