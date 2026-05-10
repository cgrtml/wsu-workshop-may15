# Washington State University — Data & Analytics Breakout
## Workshop Senaryosu (Detaylı Dakika Dakika Plan)

**Tarih:** 15 Mayıs 2026, Perşembe
**Saat:** 09:00 – 11:45 (165 dakika, çay molası dahil)
**Mekân:** WSU (Sergey hoca tarafından koordine edilecek)
**Sunucu:** Cagri Temel — Hezarfen LLC, IEEE Senior Member
**Davet:** Jeremy (program lideri), Dr. Sergey Lapin (akademik koordinatör)

**Oturum başlığı:**
> *From Black Boxes to Glass Boxes: Building Explainable Neural Trees for Safety-Critical Decisions*
> *(Kara Kutulardan Cam Kutulara: Güvenlik-Kritik Kararlar için Açıklanabilir Sinirsel Ağaçlar)*

**Hedef kitle:** WSU lisans öğrencileri (CS / Engineering / Data Science karışık seviye)
**Beklenen katılımcı sayısı:** 25–50 öğrenci

---

## Genel Akış (Bird's-eye view)

| Zaman | Süre | Bölüm | Ana mesaj |
|-------|------|-------|-----------|
| 09:00 – 09:25 | 25 dk | Açılış & Problem Framing | Bir uçak motoru ne zaman bozulur? Yanlış cevap ne demek? |
| 09:25 – 09:55 | 30 dk | Neural Trees Concept | Decision tree → soft tree → ne kazandırır? |
| 09:55 – 10:50 | 55 dk | **Activity #1: Train Your Own Neural Tree** | Hands-on Colab notebook |
| 10:50 – 11:00 | 10 dk | Çay molası | — |
| 11:00 – 11:35 | 35 dk | **Activity #2: Adversarial Sensor Challenge** | Takım yarışması |
| 11:35 – 11:45 | 10 dk | Wrap-up & Career Bridge | EU AI Act, sektör fırsatı, GitHub, LinkedIn |

---

## Bölüm 1 — Açılış & Problem Framing (09:00 – 09:25, 25 dk)

### Hedef
Öğrencileri salonda, problemi içselleştirmiş, "explainability neden önemli" sorusuna doğal olarak gelmiş halde tutmak.

### Dakika dakika

**09:00 – 09:03** (3 dk) — *Kendini tanıt, ama kısa kes.*
- "I'm Cagri Temel, founder of Hezarfen LLC, IEEE Senior Member, working on explainable AI for safety-critical industries."
- 1 cümle: GCU bağlantın, neural-trees açık kaynak paketin, NASA CMAPSS üzerine yazdığın paper.
- **Slayt:** Slide 2 (kim, ne yapıyor, neden buradayız).

**09:03 – 09:08** (5 dk) — *Hook: "Bir uçak motoru ne zaman bozulur?"*
- Slayt: Boeing 737 motor yakın çekim. "Bu motorun pisti vurmadan önce kaç uçuş döngüsü ömrü kaldığını biliyor musunuz?"
- Soru sınıfa: "Eğer bilseydik, ne yapardık?" — 2-3 öğrenciden cevap al.
- Hedef: maintenance planning, safety, cost — bunların hepsini öğrencilerin kendisi söylesin.
- **Slayt:** Slide 3-4.

**09:08 – 09:14** (6 dk) — *NASA CMAPSS dataset tanıtımı*
- "NASA bu problemi 2008'de simüle etti. Veri açık. 100 motor, her biri arızaya kadar günlük sensor okumalarıyla."
- Slayt: 21 sensör listesi — sıcaklık, basınç, fan hızı, yakıt akışı.
- RUL kavramı: Remaining Useful Life — kalan ömür (uçuş döngüsü).
- Görsel: bir motorun zaman içindeki RUL düşüşü grafiği (figures klasöründen).
- **Slayt:** Slide 5-7.

**09:14 – 09:20** (6 dk) — *Modern derin öğrenme bu işi çözüyor mu?*
- "Bir LSTM bu veri üzerinde RMSE 15.5 cycles ile RUL tahmin edebilir." Çok iyi gibi.
- Soru: "Peki FAA bu modeli sertifikalandırır mı?" — kasten boş bak, beklemesini sağla.
- Cevap: Hayır. Çünkü FAA "neden böyle dedi" sorusunun cevabını ister. LSTM bunu veremez.
- Slayt: tipik LSTM mimarisi — kasten karmaşık görünsün. "Bu kara kutudan ne çıkar?"
- **Slayt:** Slide 8-9.

**09:20 – 09:25** (5 dk) — *Black box vs glass box ayrımı*
- 2 sütunlu görsel: Black Box (LSTM, deep CNN) vs Glass Box (decision tree, linear regression).
- Trade-off: glass box genelde daha az doğru, black box yorumlanamaz.
- "Ya ikisi de olsa? Bu workshop'un sorusu bu."
- Geçiş: "Bunu nasıl yapacağımızı görmek için neural trees'e bakalım."
- **Slayt:** Slide 10.

### Bu bölümde dikkat edilecekler
- Soru-cevap interaktif olsun, monolog yapma.
- "Compliance / regulation" kelimelerini kullanmaktan çekinme — öğrencilerin çoğu sektördeki gerçek dünya kısıtlarını tanımıyor, ufuk açıyor.
- 25 dk'yı 28-30'a TAŞIMA. Concept walkthrough'a gitmeli.

---

## Bölüm 2 — Neural Trees Concept Walkthrough (09:25 – 09:55, 30 dk)

### Hedef
Öğrenciler decision tree → soft decision tree köprüsünü intuitive olarak kursunlar. Matematik abartılmasın. neural-trees paketinin orada hazır beklediğini bilsinler.

### Dakika dakika

**09:25 – 09:32** (7 dk) — *Klasik decision tree refresher*
- Tahta veya slaytta canlı bir mini ağaç çiz: "Sensor 11 (HPC outlet temp) > 480? → Sensor 14 (LPT outlet pressure) > 8.4? → Critical / Healthy"
- Kelime kelime gez: root, internal node, leaf, splitting threshold.
- "Bu ağaç çok güzel açıklıyor — ama tahmini iyi mi? Genellikle hayır. Sebep: sert (hard) split."
- **Slayt:** Slide 11-13.

**09:32 – 09:42** (10 dk) — *Hard split → soft split köprüsü*
- "Hard split: x > 480 ise sağa git." 0/1 cevap.
- Soft split: σ(w·x − b). Sigmoid. Cevap [0,1] arasında — "şu kadar olasılıkla sağa, şu kadar olasılıkla sola."
- Neden? Çünkü artık gradient akabilir → backprop ile eğitilebilir → karar ağacının yorumlanabilirliği + sinir ağının optimizasyonu birleşir.
- Slayt: aynı 2-derinlik ağacın sert vs yumuşak versiyonu, yan yana grafik.
- "Soft tree node'u küçük bir nöron gibi düşünün. Tüm ağaç → small neural network."
- **Slayt:** Slide 14-16.

**09:42 – 09:48** (6 dk) — *Neden bu safety-critical için iyi?*
- 3 maddelik özet:
  1. **Explainability:** Her tahminin yolu (path) traverse edilebilir.
  2. **Noise robustness:** Soft split, bir sensörde küçük gürültüye karşı sert split kadar hassas değil.
  3. **Sensor failure tolerance:** Channel-level dropout ile eğitildiğinde, eksik sensör girdilerine direnir.
- "Bunların hepsini birazdan kendiniz göreceksiniz — ben sadece anlatacağım sanmayın."
- **Slayt:** Slide 17-18.

**09:48 – 09:55** (7 dk) — *neural-trees package tanıtımı + Workshop akışı*
- pip install neural-trees → 30 saniyede hazır. PyPI'da, açık kaynak.
- "Bu paketi ben yazdım. Üniversite ders kitaplarındaki algoritmaları (Prof. Ethem Alpaydın) production-ready hale getirmek için."
- Github linki ve QR kod slaytta.
- "Şimdi Activity #1'e geçiyoruz. Telefonunuzu çıkarın, slaytta gördüğünüz QR kodu tarayın. Gmail hesabınızla giriş yapın."
- Sınıfta dolaş, takılan varsa yardım et.
- **Slayt:** Slide 19-20 (büyük QR kod).

### Bu bölümde dikkat edilecekler
- Matematiksel detayları minimum tut. "Sigmoid nedir?" ya da "gradient descent nedir?" sorusu gelirse çok kısa cevapla.
- 2-3 dakika fazlaya kayarsa olur — Activity #1'i 53 dk'ya kısaltabilirsin.

---

## Activity #1 — Train Your Own Neural Tree (09:55 – 10:50, 55 dk)

### Hedef
Her öğrenci kendi Colab notebook'unda CMAPSS verisiyle bir Soft Decision Tree eğitsin, decision path'i traverse etsin, ilk hands-on deneyimi yaşasın.

### Dakika dakika

**09:55 – 10:00** (5 dk) — *Setup & Onboarding*
- Slaytta büyük QR kod: `https://github.com/cgrtml/wsu-workshop-may15` landing'ine götürür.
- Landing'de iki link: Activity #1 Colab, Activity #2 Colab.
- Öğrenci: QR → landing → Activity #1 link → Colab açılır → "Copy to Drive" → kendi kopyası.
- Sen sınıfa yönelik canlı göster: ekranı yansıt, yukarıdaki adımları yap.
- **Slayt:** Slide 21 (QR + 3 adımlı kurulum).

**10:00 – 10:05** (5 dk) — *İlk hücreyi birlikte çalıştır*
- "Herkes ilk hücreyi çalıştırsın: `Runtime > Run cell` veya Shift+Enter."
- Bu hücre: pip install neural-trees + dataset wget + import'lar. ~30 saniye.
- Sınıfta dolaş — hata alanlara müdahale.
- "Hata alan var mı? Çoğunlukla 'Restart runtime' der → restart edin, sonra tekrar çalıştırın."

**10:05 – 10:15** (10 dk) — *Bölüm A: Veriyi anla ve görselleştir*
- Notebook'taki Görev 1: train_FD001.txt'i pandas ile yükle.
- Notebook'taki Görev 2: Bir motorun (engine_id=1) sensör trajektoryalarını çiz.
- Soru notebook'ta: "Motor arızaya yaklaştıkça hangi 3 sensör en çok değişiyor?"
- Sen sınıfta gez, bireysel sorulara cevap ver. Çabuk bitirenler etrafındakine yardım etsin.

**10:15 – 10:35** (20 dk) — *Bölüm B: Soft Decision Tree eğit*
- Notebook'taki Görev 3: RUL'u 3 sınıfa böl — Critical (RUL<30), Caution (30-80), Healthy (80+).
- Görev 4: Train/test split (80/20).
- Görev 5: `SoftDecisionTree(depth=4, max_epochs=30)` ile fit et.
- Görev 6: Test accuracy + confusion matrix.
- Beklenen sonuç: ~%85+ accuracy. CPU'da 30-60 saniye eğitilir.
- 5 dk önce "10 dk kaldı" uyarısı yap — geri kalanlara yetişme şansı.

**10:35 – 10:45** (10 dk) — *Bölüm C: Decision path'i traverse et (workshop'un kalbi)*
- Görev 7: Bir test motoru seç. `tree.get_split_weights()` → ağacın her node'unda hangi sensör hangi ağırlıkla.
- Görev 8: Bu motorun tahminin yolunu yazdır: "Bu motor için Sensor 11 (T24, HPC outlet) > eşik → Critical sınıfa yönelendi."
- "İşte explainability budur. Bunu LSTM ile yapamazsınız."
- Sınıfa: "Sizin motorunuzun tahmini neye göre yapıldı?" — 2-3 öğrenciden cevap.

**10:45 – 10:50** (5 dk) — *Tartışma & Geçiş*
- "Şimdi sorular: ne sürpriz oldu? hangi sensör baskındı?"
- 2-3 yorum al.
- "Çay molası. 10 dakika. 11:00'da Activity #2'ye geçiyoruz — bu sefer takım yarışması var."

### Notebook üretirken dikkat edilecekler
- 2 versiyon: `activity1_student.ipynb` (TODO'lu, eksik hücreler) ve `activity1_solution.ipynb` (tam çalışır).
- Her hücrede markdown açıklama + tek bir görev.
- CPU'da çalışır — GPU şart değil. Notebook'un en üstünde "Runtime: CPU" notu.
- Dataset Colab'ın `/content/` klasörüne wget ile gelsin — manuel upload yok.

### TA / Sergey hoca'dan istenecek yardım
- 1 TA salonda dolaşıp basit hatalara müdahale etsin (Gmail giriş sorunu, Colab not sharing, vs).
- Bu, "structured teaching with TA support" olarak EB-1A için exhibit'leşebilir.

---

## Çay Molası (10:50 – 11:00, 10 dk)

### Hedef
Öğrenciler nefes alsın, sosyalleşsin, kafalarını boşaltsın. Bu molayı atlama — 165 dk uzun.

### Sen ne yaparsın
- Sınıfta dolaş, gelen öğrencilere bireysel sorulara cevap ver.
- Sergey hoca ile kısa check-in: zaman akışı uygun mu, sonraki bölüme hazır mıyız?
- Su iç, sesini koru.

---

## Activity #2 — Adversarial Sensor Challenge (11:00 – 11:35, 35 dk)

### Hedef
Workshop'un yıldız aktivitesi. Takım yarışması formatında. "Noise-robust + explainable" mesajını öğrenciler **deneyimleyerek** öğrensin. Paper'ının Experiment 2 ve 3'ünü mini-format'ta tekrar oynat.

### Dakika dakika

**11:00 – 11:05** (5 dk) — *Senaryoyu kur*
- Slayt: "Hayali bir senaryoyu oynayalım. WSU bir havayolu şirketinin AI takımı. Bir sabah bir mesaj geliyor: motor 17'nin sensörlerinden birine drift saldırısı yapıldı. HANGİSİ?"
- "Bunu çözmek için elinizde 2 model var: bir Soft Decision Tree (sizinki, Activity #1'den), bir Random Forest baseline."
- "Doğru cevabı bulan ilk takım Hezarfen sticker kazanır." (ya da senin tercihine göre küçük ödül)

**11:05 – 11:08** (3 dk) — *Takımları kur*
- 3-4 kişilik takımlar — 8-12 takım çıkar.
- Notebook (activity2_student.ipynb) zaten herkesin Drive'ında. Aç, takımca aynı notebook'u beraber kullansınlar.

**11:08 – 11:25** (17 dk) — *Yarışma turu*
- Notebook'ta 3 farklı bozuk test seti var: `attack_A.csv`, `attack_B.csv`, `attack_C.csv`.
  - Attack A: bir sensörde sabit drift (her timestep'e +ε eklendi)
  - Attack B: bir sensörde stuck-at değer (sensor donmuş)
  - Attack C: bir sensörde gaussian noise (σ=0.3)
- Her takım her saldırı için:
  1. Hem soft tree hem random forest ile tahmin yapsın.
  2. Tahminleri "temiz veri" tahminiyle karşılaştırsın.
  3. Soft tree'nin split weights'lerini incelesin — hangi sensör baskın olmuş?
  4. Tahmin: hangi sensör manipüle edildi?
- Sen ve TA sınıfta gezin, takımlara yön gösterin (cevabı vermeden ipucu).

**11:25 – 11:30** (5 dk) — *Cevapları topla*
- Her takım hızlıca cevabını söylesin — sensör numarası + saldırı tipi.
- Sen doğru cevapları aç: A → Sensor 11 (drift), B → Sensor 14 (stuck-at), C → Sensor 9 (noise).
- Doğru bilen takımı duyur. Küçük ödül.

**11:30 – 11:35** (5 dk) — *Big picture mesaj*
- "Şimdi soru: random forest bunu yakalayabildi mi? Hayır — sadece final tahmini değişti, neden değiştiğini söyleyemedi."
- "Soft tree ne yaptı? Split weights'lerin değişimi tam olarak hangi sensörün modelin kararını etkilediğini gösterdi."
- "Bu, EU AI Act'in 'high-risk system' tanımının istediği şeyin tam olarak kendisi. Bu yüzden bu alan büyüyor."
- **Slayt:** Slide 35-37.

### Notebook üretirken dikkat
- Bozuk test setlerini önceden generate et, repo'ya commit et — students/teams direkt yüklesin.
- `activity2_solution.ipynb` cevapları içersin ama "Solution" diye işaretlensin, takımlara verilmesin.

---

## Bölüm 3 — Wrap-up & Career Bridge (11:35 – 11:45, 10 dk)

### Hedef
Öğrenciler 3 takeaway ile salondan çıksın. Senin işine sıkı bir köprü kurulsun.

### Dakika dakika

**11:35 – 11:38** (3 dk) — *3 ana mesaj*
- Slayt başlık: "What you walk out with"
- 1. **Explainability is not a luxury — it is mandatory in safety-critical AI.** EU AI Act, FDA, FAA, OCC — hepsi bunu istiyor.
- 2. **Soft Decision Trees give you both worlds:** accuracy of neural networks + interpretability of trees.
- 3. **You ran this yourself today.** Bu sahte bir demo değildi, Colab'da gerçek kod yazdınız.
- **Slayt:** Slide 38.

**11:38 – 11:42** (4 dk) — *Sektörel bağlam & fırsat*
- "Bu alan büyüyor. Banks (Model Risk Management), insurers, healthcare — hepsi explainable AI almak zorunda."
- "Mid-market US banks SR 11-7 compliance için bu tip araçları arıyor. Ben Hezarfen'de tam olarak bu pazara ürün geliştiriyorum."
- "Eğer bu konuyla ilgileniyorsanız: thesis konusu, internship, full-time — her zaman yazın."
- **Slayt:** Slide 39.

**11:42 – 11:45** (3 dk) — *Linkler ve kapanış*
- Slayt: 3 link (büyük, okunaklı):
  - GitHub: github.com/cgrtml/neural-trees
  - LinkedIn: linkedin.com/in/cagritemel
  - Email: cagritemel34@gmail.com (workshop için: cagritemelusa@gmail.com)
- "Sergey hoca'ya, Jeremy'e teşekkürler. Sorularınız varsa şimdi 5 dakika kalıyorum."
- **Slayt:** Slide 40.

---

## Pre-flight Checklist (14 Mayıs akşamı yap)

### Teknik
- [ ] Laptop tam dolu, şarj kablosu çantada.
- [ ] Adapter (HDMI / USB-C → projector). Yedek bir adapter de al.
- [ ] Slayt deck (slides.html) bilgisayarda çevrimdışı. PDF yedek.
- [ ] USB belleğe: notebook'lar, slayt PDF'i, dataset (offline backup).
- [ ] Tarayıcıda açık tab'lar: Colab notebook'ları, GitHub repo, slayt.
- [ ] Telefon hotspot hazır (wifi çökerse).
- [ ] QR kodun yazdırılmış halini cebine al — slayt çökerse hâlâ kullanabilirsin.

### İçerik
- [ ] Notebook'lar Colab'da bir kez baştan sona test edildi (bağımsız Gmail hesabıyla).
- [ ] pip install neural-trees temiz ortamda çalışıyor.
- [ ] Bozuk test setleri (attack_A/B/C.csv) repo'ya commit edildi, Colab linkten erişilebiliyor.
- [ ] Slayt'taki QR kod doğru landing URL'sine gidiyor.

### Kişisel
- [ ] Sergey hoca ile 14 Mayıs öğleden sonra final check call.
- [ ] Açılış cümlelerini sesli pratik et (3-5 dk kısmı).
- [ ] Su şişesi, atıştırmalık.

### EB-1A için belge biriktir (workshop sırasında ve sonrasında)
- [ ] Jeremy'nin davet e-postası (var, dosyala).
- [ ] Sergey hoca'dan resmi ajanda — Hezarfen ünvanı + "leading the Data & Analytics breakout" ifadesi geçsin.
- [ ] Workshop sırasında 5-10 fotoğraf çek (sen sunarken, öğrenciler aktivitelerde).
- [ ] Katılımcı sayısını Sergey hoca'dan yazılı al (e-posta yeterli).
- [ ] Slide deck'in PDF'ini arşivle.
- [ ] Notebook'ların (student + solution) PDF export'larını al.
- [ ] Workshop sonrası Sergey hoca'dan kısa bir teşekkür/değerlendirme e-postası iste — sonra letter of support'a dönüştürülebilir.
- [ ] (Mümkünse) öğrencilere kısa bir feedback formu (Google Form, 5 soru) — "did you find this useful?" gibi.

---

## Olası sorulara hazırlık

**Q: Soft tree'nin random forest'tan farkı ne?**
A: RF discrete split kullanır, ensemble. Soft tree differentiable — gradient ile öğrenir, neural network ile birleştirilebilir (örneğin LSTM'in çıktısına bağlanan bir soft tree). Paper'ımdaki TNT model tam olarak bunu yapıyor.

**Q: Bu LSTM kadar iyi mi?**
A: CMAPSS clean data'da çok yakın (RMSE 15.78 vs 15.49). Ama %30 sensör eksildiğinde LSTM %89 bozuluyor, soft tree ensemble %17. Yani trade-off çok küçük, robustness kazancı büyük.

**Q: Neden Python? R'de yok mu?**
A: PyTorch backend kullandığım için Python. R'de soft tree implementations var ama statistical comparison + scikit-learn-uyumluluk için neural-trees'i Python'da yazdım.

**Q: GPU lazım mı?**
A: CMAPSS subset için hayır. Daha büyük veri (örneğin 100K+ sample, 100+ feature) için CUDA backend var.

**Q: Bu kütüphanenin commercial kullanımı serbest mi?**
A: MIT License, tamamen serbest. Bunun üzerine ürün de geliştirilebilir.

**Q: Internship / thesis fırsatı var mı?**
A: Hezarfen LLC küçük bir şirket, formal internship programı şu an yok. Ama ilgilenen öğrenciye thesis topic önerebilirim, açık kaynak'a katkı yapabilirler — letter of recommendation gerekirse yazarım.

---

## Sonrası: Workshop sonrası 7 gün içinde

1. Sergey hoca + Jeremy'e teşekkür e-postası (kısa, profesyonel) — workshop'un nasıl geçtiğine dair 2-3 cümle, EB-1A için ileride letter of support isteyeceğini ima et (ama doğrudan isteme).
2. LinkedIn'e workshop hakkında 1 post — fotoğraflarla, neural-trees + WSU + EU AI Act narrative'i.
3. GitHub repo'yu public yap (zaten public ama README'yi cilalama).
4. EB-1A dossier'ına dosyala: davet e-postası, ajanda, fotoğraflar, katılımcı sayısı, slide PDF, notebook PDF'leri, Sergey teşekkür e-postası.
5. Repo'ya öğrencilerden gelen feedback'i sessizce gözle — eğer 1-2 öğrenci issue açar/PR yaparsa altın değerinde.

---

*Bu plan birinci versiyon. 14 Mayıs öncesi Sergey hoca ile bir kez gözden geçir, gerekirse bölüm sürelerini ±2-3 dk oynat.*
