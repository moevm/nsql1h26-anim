import { useState, useEffect, useCallback } from 'react';
import { Header } from "@components/header";
import { Button } from "@components/ui/button";
import { request } from "@api/axios"; 
import { 
  HiOutlineLocationMarker, 
  HiOutlineHeart, 
  HiOutlineChatAlt, 
  HiOutlineTrash, 
  HiOutlineX, 
  HiOutlinePlus, 
  HiOutlineArrowRight, 
  HiOutlineArrowLeft,
} from "react-icons/hi";
import styles from './FeedPage.module.css';

const PostCard = ({ post, onDelete }) => {
  const { 
    author, 
    animal, 
    tags, 
    location, 
    imageUrl, 
    title, 
    content, 
    createdAt, 
    likesCount, 
    commentsCount,
    id 
  } = post;
  
  return (
    <article className={styles.postCard}>
      {imageUrl ? (
        <div className={styles.imageContainer}>
          <img src={imageUrl} alt={title} className={styles.postImage} />
        </div>
      ) : (
        <div className={styles.imagePlaceholder}>Нет фото</div>
      )}
      
      <div className={styles.cardBody}>
        <div className={styles.authorSection}>
          <div className={styles.authorAvatar}>
            {author?.username?.slice(0, 2).toUpperCase() || '??'}
          </div>
          <div className={styles.authorInfo}>
            <span className={styles.authorName}>{author?.username || 'Инкогнито'}</span>
            <span className={styles.postDate}>
              {createdAt ? new Date(createdAt).toLocaleDateString() : 'Недавно'}
            </span>
          </div>
        </div>

        <div className={styles.postContent}>
          <h3 className={styles.postTitle}>{title}</h3>
          {animal && (
            <div className={styles.animalTag}>
              <strong>{animal.name}</strong> <i>{animal.scientificName}</i>
            </div>
          )}
          <p className={styles.postDescription}>{content}</p>
          
          <div className={styles.hashtags}>
            {tags?.map((tag, idx) => (
              <span key={idx} className={styles.hashtag}>#{tag}</span>
            ))}
          </div>

          {location && (
            <div className={styles.location}>
              <HiOutlineLocationMarker /> {location}
            </div>
          )}

          <div className={styles.postStats}>
            <div className={styles.statGroup}>
              <span className={styles.statItem}><HiOutlineHeart /> {likesCount || 0}</span>
              <span className={styles.statItem}><HiOutlineChatAlt /> {commentsCount || 0}</span>
            </div>
            <HiOutlineTrash className={styles.deleteBtn} onClick={() => onDelete(id)} />
          </div>
        </div>
      </div>
    </article>
  );
};

export const FeedPage = () => {
  const [posts, setPosts] = useState([]);
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [step, setStep] = useState(1);
  const [activeTab, setActiveTab] = useState('note');
  const [loading, setLoading] = useState(false);
  const [fetching, setFetching] = useState(true);

  const [formData, setFormData] = useState({
    title: '', content: '', location: '', 
    imageUrl: '', tags: '', animalName: '', scientificName: ''
  });

  const fetchPosts = useCallback(async () => {
    setFetching(true);
    try {
      const data = await request('GET', '/posts'); 
      setPosts(Array.isArray(data) ? data : []);
    } catch (error) {
      console.error("Ошибка загрузки:", error);
    } finally {
      setFetching(false);
    }
  }, []);

  useEffect(() => {
    fetchPosts();
  }, [fetchPosts]);

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({ ...prev, [name]: value }));
  };

  const handleClose = () => {
    setIsModalOpen(false);
    setStep(1);
    setFormData({ 
      title: '', 
      content: '', 
      location: '', 
      imageUrl: '', 
      tags: '', 
      animalName: '', 
      scientificName: '' 
    });
  };

  const handleSubmit = async () => {
    setLoading(true);
    try {
      const payload = {
        title: formData.title,
        content: formData.content,
        imageUrl: formData.imageUrl || null,
        location: formData.location || null,
        type: activeTab === 'note' ? 'note' : 'animal',
        tags: formData.tags ? formData.tags.split(',').map(t => t.trim().toLowerCase()).filter(Boolean) : [],
        animal: activeTab === 'animal' ? {
          name: formData.animalName,
          scientificName: formData.scientificName || formData.animalName 
        } : null,
        taxon: activeTab === 'animal' ? { name: "Animalia", rank: "kingdom" } : null 
      };

      await request('POST', '/posts', payload);
      handleClose();
      fetchPosts();
    } catch (error) {
      alert("Ошибка при сохранении");
    } finally {
      setLoading(false);
    }
  };

  const handleSeed = () => {
    const testAnimals = [
      { 
        name: "Благородный олень", 
        sci: "Cervus elaphus", 
        tags: "олень, лес, копытные", 
        loc: "Лосиный остров",
        img: "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTKp4kj7OeR_pR41Nr2FUH1Ug9Z2RpS079QGqjeK7bkeUW9mFHWu6FFxCNA-Kbklopxo7XRXtVrwHE79fd-OlD_NYWOPRIOc6DPHGUnXQ&s=10"
      },
      { 
        name: "Бурый медведь", 
        sci: "Ursus arctos", 
        tags: "медведь, тайга, хищник", 
        loc: "Камчатка",
        img: "https://images.unsplash.com/photo-1589656966895-2f33e7653819?auto=format&fit=crop&q=80&w=800"
      },
      { 
        name: "Серый волк", 
        sci: "Canis lupus", 
        tags: "волк, стая, лес", 
        loc: "Карелия",
      },
      { 
        name: "Обыкновенная лисица", 
        sci: "Vulpes vulpes", 
        tags: "лиса, поле", 
        loc: "Подмосковье",
        img: "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQ4xa1Wfyiamf5LdGzL38oGQyqltBYgArtM8yw5llpPEpOVm3vPt0dxyOQb2FRMqYkiILkfrvA0uis6B-PdOCgi9e_SyxgN9UvMBbu1mKU&s=10"
      },
      { 
        name: "Хозяин Арктики", 
        sci: "Lynx lynx", 
        tags: "белый, арктика, медведь", 
        loc: "Сибирь",
        img: "https://images.unsplash.com/photo-1589656966895-2f33e7653819?q=80&w=800"
      },
      { 
        name: "Лось", 
        sci: "Alces alces", 
        tags: "лось, болото", 
        loc: "Ленинградская область",
        img: "https://images.unsplash.com/photo-1589182373726-e4f658ab50f0?auto=format&fit=crop&q=80&w=800"
      },
      { 
        name: "Кабан", 
        sci: "Sus scrofa", 
        tags: "кабан, лес, всеядные", 
        loc: "Тверская область",
        img: "https://upload.wikimedia.org/wikipedia/commons/thumb/3/3d/Ausgewachsenes_Wildschwein_beim_Suhlen.JPG/960px-Ausgewachsenes_Wildschwein_beim_Suhlen.JPG"
      },
      { 
        name: "Заяц-русак", 
        sci: "Lepus europaeus", 
        tags: "заяц, ушастый", 
        loc: "Ростовская область",
        img: "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSn8ue6EbnWSV6J2eqUf3fDHv7o9Ao8plavU9Ah7oKlePo67Bw-TzDy2acuypKS6Sw0XpKYP0nZt7NQaZq6CmVXQWjacBwAkdrjlBG25hzV2A&s=10"
      },
      { 
        name: "Обыкновенная белка", 
        sci: "Sciurus vulgaris", 
        tags: "белка, парк, грызуны", 
        loc: "Парк Сокольники",
        img: "https://images.unsplash.com/photo-1507666405895-422eee7d517f?auto=format&fit=crop&q=80&w=800"
      },
      { 
        name: "Амурский тигр", 
        sci: "Panthera tigris altaica", 
        tags: "тигр, красная книга",
        loc: "Приморский край",
        img: "https://images.unsplash.com/photo-1561731216-c3a4d99437d5?auto=format&fit=crop&q=80&w=800"
      }
    ];

    const randomAnimal = testAnimals[Math.floor(Math.random() * testAnimals.length)];

    const seedData = {
      title: `Встреча с дикой природой: ${randomAnimal.name}`,
      content: `Удалось зафиксировать особь вида ${randomAnimal.sci} в естественной среде. Поведение спокойное, угрозы не обнаружено. Данные добавлены в рамках тестирования базы.`,
      location: randomAnimal.loc,
      imageUrl: randomAnimal.img,
      animalName: randomAnimal.name,
      scientificName: randomAnimal.sci,
      tags: randomAnimal.tags
    };

    setFormData(seedData);
    setActiveTab('animal');
    setIsModalOpen(true);
  };

  const handleDelete = async (postId) => {
    if (!window.confirm("Удалить запись?")) return;
    try {
      await request('DELETE', `/posts/${postId}`);
      setPosts(prev => prev.filter(p => p.id !== postId));
    } catch (error) {
      alert("Ошибка удаления");
    }
  };

  return (
    <div className={styles.feedWrapper}>
      <Header />
      <main className={styles.mainContent}>
        <div className={styles.lentaHeader}>
          <div>
            <h2 className={styles.lentaTitle}>Лента наблюдений</h2>
            <p className={styles.lentaSubtitle}>Делитесь своими открытиями дикой природы</p>
          </div>
          <Button onClick={() => handleSeed()} style={{'width': '300px'}}>Кнопка с подстановкой</Button>
          <Button onClick={() => setIsModalOpen(true)} className={styles.addPost}>
            <HiOutlinePlus /> Добавить запись
          </Button>
        </div>

        <div className={styles.counterWrapper}>
          <p>Показано <span className={styles.counterNumber}>{posts.length}</span> наблюдений</p>
        </div>

        {fetching ? (
          <div className={styles.loadingState}>Загрузка ленты...</div>
        ) : (
          <div className={styles.postsList}>
            {posts.map((post) => (
              <PostCard key={post.id || Math.random()} post={post} onDelete={handleDelete} />
            ))}
          </div>
        )}
      </main>

      {isModalOpen && (
        <div className={styles.modalOverlay} onClick={handleClose}>
          <div className={styles.modalContent} onClick={e => e.stopPropagation()}>
            <div className={styles.modalHeader}>
              <div className={styles.modalTitleBox}>
                <h3 className={styles.modalHeading}>Новая запись</h3>
                <span className={styles.stepIndicator}>{step}/2</span>
              </div>
              <button className={styles.closeIconBtn} onClick={handleClose}><HiOutlineX /></button>
            </div>

            <div className={styles.modalBody}>
              {step === 1 ? (
                <>
                  <div className={styles.typeSelector}>
                    <button 
                      type="button"
                      className={activeTab === 'note' ? styles.tabActive : styles.tabDefault} 
                      onClick={() => setActiveTab('note')}
                    >Заметка</button>
                    <button 
                      type="button"
                      className={activeTab === 'animal' ? styles.tabActive : styles.tabDefault} 
                      onClick={() => setActiveTab('animal')}
                    >Наблюдение</button>
                  </div>

                  {activeTab === 'animal' && (
                    <div className={styles.animalFieldsAnim}>
                      <div className={styles.fieldGroup}>
                        <label className={styles.label}>ЖИВОТНОЕ</label>
                        <input className={styles.input} name="animalName" value={formData.animalName} onChange={handleInputChange} placeholder="Напр. Благородный олень" />
                      </div>
                      <div className={styles.fieldGroup}>
                        <label className={styles.label}>LATIN NAME</label>
                        <input className={styles.input} name="scientificName" value={formData.scientificName} onChange={handleInputChange} placeholder="Cervus elaphus" />
                      </div>
                    </div>
                  )}

                  <div className={styles.fieldGroup}>
                    <label className={styles.label}>ЗАГОЛОВОК *</label>
                    <input className={styles.input} name="title" value={formData.title} onChange={handleInputChange} placeholder="О чем ваша запись?" />
                  </div>

                  <div className={styles.fieldGroup}>
                    <label className={styles.label}>ОПИСАНИЕ *</label>
                    <textarea className={styles.textarea} name="content" value={formData.content} onChange={handleInputChange} placeholder="Расскажите подробности..." />
                  </div>

                  <div className={styles.modalFooter}>
                    <button className={styles.textBtn} onClick={handleClose}>Отмена</button>
                    <button className={styles.primaryBtn} onClick={() => setStep(2)}>
                      Далее <HiOutlineArrowRight />
                    </button>
                  </div>
                </>
              ) : (
                <>
                  <div className={styles.fieldGroup}>
                    <label className={styles.label}>URL ИЗОБРАЖЕНИЯ</label>
                    <input className={styles.input} name="imageUrl" value={formData.imageUrl} onChange={handleInputChange} placeholder="https://unsplash.com/..." />
                  </div>

                  <div className={styles.fieldGroup}>
                    <label className={styles.label}>ТЕГИ (ЧЕРЕЗ ЗАПЯТУЮ)</label>
                    <input className={styles.input} name="tags" value={formData.tags} onChange={handleInputChange} placeholder="лес, туман, утро" />
                  </div>

                  <div className={styles.fieldGroup}>
                    <label className={styles.label}>МЕСТОПОЛОЖЕНИЕ</label>
                    <input className={styles.input} name="location" value={formData.location} onChange={handleInputChange} placeholder="Напр. Лосиный остров" />
                  </div>

                  <div className={styles.modalFooter}>
                    <button className={styles.textBtn} onClick={() => setStep(1)}>
                      <HiOutlineArrowLeft /> Назад
                    </button>
                    <button className={styles.primaryBtn} onClick={handleSubmit} disabled={loading}>
                      {loading ? 'Публикация...' : 'Опубликовать'}
                    </button>
                  </div>
                </>
              )}
            </div>
          </div>
        </div>
      )}
    </div>
  );
};