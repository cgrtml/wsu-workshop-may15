# Washington State University — Data & Analytics Breakout
## Workshop Senaryosu (Detaylı Dakika Dakika Plan)

**Tarih:** 15 Mayıs 2026, Perşembe
**Saat:** 09:00 – 11:45 (165 dakika, çay molası dahil)
**Mekân:** WSU (Sergey hoca tarafından koordine edilecek)
**Co-presenters:**
  - **Sundar Krishnamurthy** — Security Engineering Leader, Expedia Group · CISSP
  - **Cagri Temel** — CTO, Hezarfen LLC · IEEE Senior Member

**Davet:** Jeremy (program lideri), Dr. Sergey Lapin (akademik koordinatör)

**Joint oturum başlığı:**
> *Data & Analytics Breakout — Cagri & Sundar*

**Cagri'nin segmentinin başlığı:**
> *From Black Boxes to Glass Boxes: Building Explainable Neural Trees for Safety-Critical Decisions*

**Konunun çerçevesi:** Workshop tamamen senin uzmanlık alanın — explainable ML + predictive maintenance + NASA CMAPSS turbofan engine RUL tahmini. Sundar'ın security segmentine sadece **bir köprü cümlesi** kuruluyor: "fault detection tekniği hem hardware failure hem adversarial attack için aynı şekilde işliyor." Security ana tema değil.

**Hedef kitle:** WSU lisans öğrencileri (CS / Engineering / Data Science karışık seviye)
**Beklenen katılımcı sayısı:** 25–50 öğrenci

---

## Genel Akış (Bird's-eye view)

| Zaman | Süre | Kim | Bölüm |
|-------|------|-----|-------|
| 09:00 – 09:10 | 10 dk | **Joint** | Açılış: "Why Trust Matters in Safety-Critical Systems" |
| 09:10 – 09:50 | 40 dk | **Sundar** | Industry security landscape (Expedia stories, threat modeling) |
| 09:50 – 10:00 | 10 dk | **Joint** | Geçiş köprüsü + Q&A — "From systems security to AI security" |
| 10:00 – 10:50 | 50 dk | **Cagri** | Activity #1 — Train Your Own Neural Tree |
| 10:50 – 11:00 | 10 dk | — | ☕ Çay molası |
| 11:00 – 11:25 | 25 dk | **Cagri** | Activity #2 — Sensor Fault Detection Challenge |
| 11:25 – 11:40 | 15 dk | **Cagri** | 🔧 GitHub Contribution Sprint |
| 11:40 – 11:45 | 5 dk | **Joint** | Closing + her iki taraftan contact info |

**Cagri'nin toplam payı:** ~95 dakika hands-on + GitHub sprint (önceki plandan kayıp yok, security framing ile ekstra güç).

---

## Bölüm 0 — Joint Açılış (09:00 – 09:10, 10 dk)

### Hedef
Salon ısınsın, iki sunucu kendini kısaca tanıtsın, programın tonu kurulsun.

### Akış
- **Sergey hoca veya Jeremy** sizi takdim eder (1-2 dk).
- **Sundar** kendini tanıtır (2-3 dk): Expedia, security background.
- **Cagri** kendini tanıtır (2-3 dk): Hezarfen, IEEE Senior Member, neural-trees, paper.
- Joint çerçeveleme: "Bugün iki tarafı göreceksiniz — endüstride sistem güvenliği (Sundar) + AI sistemlerinin güvenliği (Cagri). İkisi de aynı problemin farklı yüzleri."

### Sen ne yaparsın
- Kısa ve enerjik tut. 3 dakika sınırına dikkat — Sundar'a 40 dakikalık alan açmalısın.
- Sundar'la önceden Zoom'da bir cümle prova edin: "geçiş cümlesi" ne olacak.

---

## Bölüm 1 — Sundar's Segment (09:10 – 09:50, 40 dk)

### Sen ne yaparsın
- **Sundar sunarken sen sahnede değilsin.** Salonun arkasına geç, dinleyen pozisyonunda ol.
- Yine de **dikkatle dinle** — Sundar'ın spesifik örneklerini not et, kendi segmentinde "as Sundar mentioned…" diyebilmek için.
- Q&A bölümünde Sundar'a destek ol — bir öğrenci AI/ML soru sorarsa Sundar geri dönerse müdahale et.

### Sundar'ın muhtemel içeriği (Zoom'da netleşecek)
- Endüstride attack landscape: data breach, supply chain, insider threats
- Threat modeling frameworks: STRIDE, MITRE ATT&CK
- Real-world Expedia-scale stories (anonymized)
- Career advice: cybersecurity'de nasıl başlanır

---

## Bölüm 2 — Joint Köprü + Q&A (09:50 – 10:00, 10 dk)

### Hedef
Sundar'ın konusundan senin konuna doğal geçiş kur.

### Akış
- Sundar'ın anahtar mesajını özetle: "Sundar showed us how attackers target systems, data, and infrastructure."
- Köprü cümlesi: "Now I want to show you how attackers target the AI MODELS themselves — and how we defend by making models that explain their own decisions."
- 2-3 öğrenci sorusu al (joint cevap).
- Activity #1'e geçişe hazırlan.

### Slayt
- Slide 11-12: Joint çerçeveleme, "Three layers of attack: infrastructure → data → model"

---

## Activity #1 — Train Your Own Neural Tree (10:00 – 10:50, 50 dk)

### Hedef
Her öğrenci kendi Colab notebook'unda CMAPSS verisiyle bir Soft Decision Tree eğitsin, decision path'i traverse etsin.

### Dakika dakika

**10:00 – 10:05** (5 dk) — *Setup & Onboarding*
- Slaytta büyük QR kod: `https://github.com/cgrtml/wsu-workshop-may15` landing'ine götürür.
- Landing'de iki link: Activity #1 Colab, Activity #2 Colab.
- Öğrenci: QR → landing → Activity #1 link → Colab açılır → "Copy to Drive" → kendi kopyası.
- Sen sınıfa yönelik canlı göster: ekranı yansıt, yukarıdaki adımları yap.

**10:05 – 10:10** (5 dk) — *İlk hücreyi birlikte çalıştır*
- "Herkes ilk hücreyi çalıştırsın: Shift+Enter."
- Bu hücre: pip install neural-trees + dataset wget + import'lar. ~30 saniye.
- Sınıfta dolaş — hata alanlara müdahale.
- "Hata alan var mı? Çoğunlukla 'Restart runtime' der → restart edin, sonra tekrar çalıştırın."

**10:10 – 10:18** (8 dk) — *Bölüm A: Veriyi anla ve görselleştir*
- Notebook'taki Görev 1: train_FD001.txt'i pandas ile yükle.
- Notebook'taki Görev 2: Bir motorun (engine_id=1) sensör trajektoryalarını çiz.
- Soru notebook'ta: "Motor arızaya yaklaştıkça hangi 3 sensör en çok değişiyor?"

**10:18 – 10:35** (17 dk) — *Bölüm B: Soft Decision Tree eğit*
- Görev 3: RUL'u 3 sınıfa böl — Critical (RUL<30), Caution (30-80), Healthy (80+).
- Görev 4: Train/test split (80/20).
- Görev 5: `SoftDecisionTree(depth=4, max_epochs=30)` ile fit et.
- Görev 6: Test accuracy + confusion matrix.
- Beklenen sonuç: ~%85+ accuracy. CPU'da 30-60 saniye eğitilir.

**10:35 – 10:45** (10 dk) — *Bölüm C: Decision path'i traverse et (workshop'un kalbi)*
- Görev 7: Bir test motoru seç. `tree.get_split_weights()` → ağacın her node'unda hangi sensör hangi ağırlıkla.
- Görev 8: Bu motorun tahminin yolunu yazdır: "Bu motor için Sensor 11 (T24, HPC outlet) > eşik → Critical sınıfa yönelendi."
- "İşte explainability budur. Bunu LSTM ile yapamazsınız."

**10:45 – 10:50** (5 dk) — *Tartışma & Geçiş*
- "Şimdi sorular: ne sürpriz oldu? hangi sensör baskındı?"
- 2-3 yorum al.
- "Çay molası. 10 dakika. 11:00'da Activity #2'ye geçiyoruz — bu sefer **takım yarışması + AI security** var."

### Notebook üretirken dikkat
- 2 versiyon: `activity1_student.ipynb` (TODO'lu) ve `activity1_solution.ipynb`.
- Her hücrede markdown açıklama + tek bir görev.
- CPU'da çalışır — GPU şart değil.

---

## Çay Molası (10:50 – 11:00, 10 dk)

### Sen ne yaparsın
- Sınıfta dolaş, gelen öğrencilere bireysel sorulara cevap ver.
- Sundar ile kısa check-in: zaman akışı uygun mu, sonraki bölüme hazır mıyız?
- Su iç, sesini koru.

---

## Activity #2 — Sensor Fault Detection Challenge (11:00 – 11:25, 25 dk)

### Hedef
Workshop'un yıldız aktivitesi. Takım yarışması formatında. **Predictive maintenance / sensor fault localization** ana çerçeve — bu senin uzmanlık alanın. Security ile bağlantı sadece kapanışta bir cümle.

### Dakika dakika

**11:00 – 11:04** (4 dk) — *Senaryoyu kur*
- Slayt: "Engine 17'nin sensörlerinden birinde bir şey ters gidiyor — drift, stuck-at, ya da gürültü artışı. Hangi sensör? Modelin sana söyleyebilir mi?"
- Predictive maintenance bağlamı: "Sensörler her gün arızalanır. Hardware aging, calibration drift, noise spikes — bunlar gerçek operasyonel problemler."
- Kapanış cümlesi: "Bu teknik adversarial attack için de aynı şekilde işliyor — ki Sundar'ın bu sabah bahsettiği tarafa da bağlanıyor."
- "Doğru cevabı bulan ilk takım Hezarfen sticker kazanır."

**11:04 – 11:06** (2 dk) — *Takımları kur*
- 3-4 kişilik takımlar.
- activity2_student.ipynb herkesin Drive'ında. Aç, takımca aynı notebook'u beraber kullansınlar.

**11:06 – 11:18** (12 dk) — *Yarışma turu*
- Her takım her saldırı için:
  1. Hem soft tree hem random forest ile tahmin yapsın.
  2. Tahminleri "temiz veri" tahminiyle karşılaştırsın.
  3. Soft tree'nin split weights'lerini incelesin — hangi sensör baskın olmuş?
  4. Tahmin: hangi sensör manipüle edildi?
- Sen ve Sundar (varsa TA) sınıfta gezin — Sundar'ın salonda olması teknik dolaşımı zenginleştirir.

**11:18 – 11:22** (4 dk) — *Cevapları topla*
- Her takım hızlıca cevabını söylesin.
- Doğru cevaplar: A → Sensor 11 (drift), B → Sensor 14 (stuck-at), C → Sensor 9 (noise).
- Doğru bilen takımı duyur.

**11:22 – 11:25** (3 dk) — *Big picture mesaj*
- "Random forest tahminini değiştirdi ama nedenini söyleyemedi. Soft tree'nin split weights'leri tam olarak hangi sensörün modelin kararını etkilediğini gösterdi."
- "Bu, predictive maintenance için temel bir capability. EU AI Act'in 'high-risk system' tanımının istediği şey — ve aynı teknik adversarial attack detection için de işliyor (Sundar'ın bu sabah bahsettiği taraf)."

---

## 🔧 GitHub Contribution Sprint (11:25 – 11:40, 15 dk)

### Hedef
Workshop'un **EB-1A için en güçlü segmenti**. Öğrenciler senin neural-trees library'sine **gerçek katkı** yapsın. Sonuç: 10-20 yeni contributor, GitHub history'sinde 15 Mayıs 2026 tarihli, sen merge eden olarak görüneceksin.

### Ön hazırlık (Workshop'tan önce — 12-13 Mayıs)
- `cgrtml/neural-trees` repo'sunda 15-20 tane **"good first issue"** etiketli issue açılı olmalı:
  - "Add a docstring example to `SoftDecisionTree.fit()`"
  - "Write a unit test for `combined_5x2cv_f_test`"
  - "Add usage example notebook for HierarchicalMixtureOfExperts"
  - "Fix typo in README line X"
  - "Add type hints to `predict_proba`"
  - "Add a CITATION.cff file"
  - "Add Python 3.12 to CI matrix"
  - "Improve error message when X happens"
  - vs.
- `CONTRIBUTING.md` hazır olmalı — beginner-friendly, "fork → branch → commit → PR" akışı.
- Bir "WSU Workshop Contributors" recognition section README'ye eklenmiş olmalı (boş, sonra dolacak).

### Dakika dakika

**11:25 – 11:28** (3 dk) — *Sprint'i tanıt*
- Slayt: "Want a real GitHub contribution to a published ML library on your profile? You have 15 minutes."
- Adımlar: (1) github.com/cgrtml/neural-trees → Issues → "good first issue" filter → bir issue claim et (yorumla). (2) Repo'yu fork et. (3) Codespaces aç (1 tıklama, ücretsiz) — VEYA tarayıcıda direkt edit et (basit issue'lar için).
- "Sınıfta dolaşıp yardım edeceğim. PR açtığınızda direkt review başlatacağım."

**11:28 – 11:38** (10 dk) — *Hands-on contribution*
- Öğrenciler issue'ları seçer, fork eder, değişiklik yapar, PR açar.
- Sen sınıfta gez, GitHub PR sayfasını yansıtarak canlı review yap — "label-typo" gibi basit PR'ları **canlı merge** et.
- Hedef: workshop bitmeden 5-10 PR merged olsun.

**11:38 – 11:40** (2 dk) — *Sonuç*
- Slayt: "GitHub.com/cgrtml/neural-trees/contributors" sayfasını canlı yansıt — yeni contributor'lar görünür.
- "Bunlar artık sizin profilinizde. CV'nize, internship başvurularınıza koyabilirsiniz."

### EB-1A için bu segmentten çıkacak kanıtlar
- 15 Mayıs 2026 tarihli 10-20 PR (neural-trees commit history)
- Senin merge commit'lerin (judging kanıtı)
- "WSU Workshop Contributors" README section'ında isim listesi
- GitHub contributors page screenshot'u (workshop öncesi vs sonrası)
- Sergey hoca'dan letter: "Cagri Temel led an open-source development sprint where X students submitted PRs to his neural-trees library, demonstrating both his technical leadership and pedagogical contribution to WSU students."

---

## Bölüm 3 — Joint Closing (11:40 – 11:45, 5 dk)

### Akış
- Sundar kapanış cümlesi (1 dk): kendi segmentinden ana çıkarım.
- Cagri kapanış cümlesi (1 dk): "What you walk out with."
- Slayt: 4 link (büyük) — github.com/cgrtml/neural-trees, github.com/cgrtml/wsu-workshop-may15, Sundar LinkedIn, Cagri LinkedIn.
- "Sergey hoca'ya, Jeremy'e teşekkürler. Sorularınız varsa şimdi 5 dakika kalıyoruz."

### 3 ana mesaj (slaytta, kapanışta vurgu)
1. **Security and AI safety are converging.** What Sundar showed for systems is what Cagri showed for models.
2. **Explainability is not a luxury — it's a defensive capability.**
3. **You ran this yourself today, and some of you contributed to a real OSS project.**

---

## Pre-flight Checklist (14 Mayıs akşamı yap)

### Teknik
- [ ] Laptop tam dolu, şarj kablosu çantada.
- [ ] Adapter (HDMI / USB-C → projector). Yedek bir adapter de al.
- [ ] Slayt deck (slides.html) bilgisayarda çevrimdışı. PDF yedek.
- [ ] USB belleğe: notebook'lar, slayt PDF'i, dataset (offline backup).
- [ ] Tarayıcıda açık tab'lar: Colab notebook'ları, GitHub repo, slayt, neural-trees Issues sayfası.
- [ ] Telefon hotspot hazır (wifi çökerse).
- [ ] QR kodun yazdırılmış halini cebine al.

### İçerik
- [ ] Notebook'lar Colab'da bir kez baştan sona test edildi (bağımsız Gmail hesabıyla).
- [ ] pip install neural-trees temiz ortamda çalışıyor.
- [ ] Bozuk test setleri (attack_A/B/C.csv) repo'ya commit edildi, Colab linkten erişilebiliyor.
- [ ] Slayt'taki QR kod doğru landing URL'sine gidiyor.
- [ ] **neural-trees repo'sunda 15-20 "good first issue" hazır.**
- [ ] **CONTRIBUTING.md neural-trees repo'sunda yayında.**
- [ ] **README'de "WSU Workshop Contributors" placeholder section var.**

### Sundar koordinasyonu
- [ ] Sundar ile Zoom call'da time split netleşti.
- [ ] Geçiş cümleleri (10 → 11, 11 → 12 arası) prova edildi.
- [ ] Sundar'ın slaytlarına göz attın (varsa) — duplikasyon yok.

### Kişisel
- [ ] Sergey hoca ile 14 Mayıs öğleden sonra final check call.
- [ ] Açılış cümlelerini sesli pratik et.
- [ ] Su şişesi, atıştırmalık.

### EB-1A için belge biriktir
- [ ] Jeremy'nin davet e-postası (var, dosyala).
- [ ] Sergey hoca'dan resmi ajanda — Hezarfen ünvanı + "leading the AI Security & Explainability segment" ifadesi geçsin.
- [ ] Workshop sırasında 5-10 fotoğraf çek (sen sunarken, öğrenciler aktivitelerde, GitHub sprint sırasında).
- [ ] Katılımcı sayısını Sergey hoca'dan yazılı al.
- [ ] Slide deck'in PDF'ini arşivle.
- [ ] Notebook'ların PDF export'larını al.
- [ ] **neural-trees repo'sunun "Insights → Contributors" sayfasının screenshot'u (workshop öncesi)**
- [ ] **Aynı sayfanın workshop sonrası screenshot'u — fark görsel kanıt**
- [ ] Workshop sonrası Sergey hoca'dan kısa bir teşekkür/değerlendirme e-postası iste.
- [ ] Sundar'dan da kısa bir e-posta iste — "great co-presenting with you" tarzı, sonradan letter of support için bağlantı.

---

## Olası sorulara hazırlık

**Q: Soft tree'nin random forest'tan farkı ne?**
A: RF discrete split kullanır, ensemble. Soft tree differentiable — gradient ile öğrenir, neural network ile birleştirilebilir. Paper'ımdaki TNT model tam olarak bunu yapıyor.

**Q: Bu LSTM kadar iyi mi?**
A: CMAPSS clean data'da çok yakın (RMSE 15.78 vs 15.49). Ama %30 sensör eksildiğinde LSTM %89 bozuluyor, soft tree ensemble %17.

**Q: GPU lazım mı?**
A: CMAPSS subset için hayır. CPU'da hızlı eğitilir.

**Q: Bu kütüphanenin commercial kullanımı serbest mi?**
A: MIT License, tamamen serbest.

**Q: Internship / thesis fırsatı var mı?**
A: Hezarfen LLC küçük bir şirket, formal internship programı şu an yok. Ama ilgilenen öğrenciye thesis topic önerebilirim, açık kaynak'a katkı yapabilirler.

**Q: Soft decision tree adversarial attack'lara ne kadar dayanıklı?**
A: Bu workshop'un Activity #2'sinde gördüğümüz gibi — sensor manipülasyonuna karşı RF'den daha okunaklı bir cevap veriyor (split weights değişiyor). Tam adversarial robustness için ek savunmalar gerek (input validation, ensembling, certified bounds). Ama explainability tek başına bir defense layer.

---

## Sonrası: Workshop sonrası 7 gün içinde

1. Sergey hoca + Jeremy + Sundar'a teşekkür e-postası.
2. **neural-trees repo'sundaki student PR'larının kalanını review et + merge et.**
3. **README'deki "WSU Workshop Contributors" section'ını güncel isim listesiyle doldur.**
4. LinkedIn'e workshop hakkında 1 post — fotoğraflarla, neural-trees + WSU + EU AI Act + AI Security narrative'i.
5. EB-1A dossier'ına dosyala: davet e-postası, ajanda, fotoğraflar, katılımcı sayısı, slide PDF, notebook PDF'leri, contributors page screenshot'ları, Sergey/Sundar teşekkür e-postaları.

---

*Bu plan 2. versiyon — Sundar Krishnamurthy ile co-presenting kurgusu. 14 Mayıs öncesi Sergey hoca + Sundar ile Zoom'da bir kez gözden geçir.*
