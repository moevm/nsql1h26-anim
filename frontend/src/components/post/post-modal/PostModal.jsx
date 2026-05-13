import { useState, useEffect, useRef } from 'react';
import {
  HiOutlineX, HiOutlineCamera, HiOutlineLocationMarker,
  HiOutlinePencilAlt, HiOutlinePhotograph
} from "react-icons/hi";
import styles from './PostModal.module.css';

const TAXON_OPTIONS = [
  { value: 'mammal', label: 'Млекопитающее' },
  { value: 'bird', label: 'Птица' },
  { value: 'reptile', label: 'Рептилия' },
  { value: 'amphibian', label: 'Земноводное' },
  { value: 'fish', label: 'Рыба' },
  { value: 'invertebrate', label: 'Беспозвоночное' },
];

const EMPTY_FORM = {
  title: '', content: '', location: '',
  imageUrl: '', tags: '', animalName: '',
  scientificName: '', taxon: 'mammal',
};

export const PostModal = ({ isOpen, onClose, onSubmit, loading, post = null }) => {
  const isEdit = !!post;
  const [step, setStep] = useState(1);
  const [activeTab, setActiveTab] = useState('note');
  const [formData, setFormData] = useState(EMPTY_FORM);
  const createDraftRef = useRef(EMPTY_FORM);

  useEffect(() => {
    if (!isOpen) return;

    if (isEdit && post) {
      setFormData({
        title: post.title || '',
        content: post.content || '',
        location: post.location || '',
        imageUrl: post.imageUrl || '',
        tags: post.tags?.join(', ') || '',
        animalName: post.animal?.name || '',
        scientificName: post.animal?.scientificName || '',
        taxon: post.animal?.taxon || 'mammal',
      });
      setActiveTab(post.type || 'note');
      setStep(1);
    } else {
      setFormData(createDraftRef.current);
    }
  }, [isOpen]);

  if (!isOpen) return null;

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => {
      const next = { ...prev, [name]: value };
      if (!isEdit) createDraftRef.current = next;
      return next;
    });
  };

  const handleTabChange = (tab) => {
    setActiveTab(tab);
    if (!isEdit) createDraftRef.current = { ...createDraftRef.current };
  };

  const handleClose = () => {
    if (isEdit) {
      setFormData({
        title: post.title || '',
        content: post.content || '',
        location: post.location || '',
        imageUrl: post.imageUrl || '',
        tags: post.tags?.join(', ') || '',
        animalName: post.animal?.name || '',
        scientificName: post.animal?.scientificName || '',
        taxon: post.animal?.taxon || 'mammal',
      });
      setActiveTab(post.type || 'note');
    }
    onClose();
  };

  const handleSubmit = (e) => {
    e.preventDefault();

    const payload = {
      title: formData.title.trim(),
      content: formData.content.trim(),
      location: formData.location.trim() || null,
      image_url: formData.imageUrl.trim() || null,
      tags: formData.tags
        ? formData.tags.split(',').map(t => t.trim()).filter(Boolean)
        : [],
      type: activeTab,
    };

    if (activeTab === 'animal') {
      payload.animal = {
        name: formData.animalName.trim(),
        scientific_name: formData.scientificName.trim() || null,
        taxon: formData.taxon,
      };
    } else {
      payload.animal = null;
    }

    onSubmit(payload);

    if (!isEdit) {
      createDraftRef.current = EMPTY_FORM;
      setFormData(EMPTY_FORM);
      setStep(1);
      setActiveTab('note');
    }
  };

  return (
    <div className={styles.modalOverlay}>
      <div className={styles.modalContent}>
        <div className={styles.modalHeader}>
          <h2>
            {isEdit
              ? 'Редактировать пост'
              : step === 1 ? 'Создать публикацию' : 'Детали публикации'}
          </h2>
          <button className={styles.closeBtn} onClick={handleClose}>
            <HiOutlineX />
          </button>
        </div>

        <form onSubmit={handleSubmit} className={styles.form}>
          {step === 1 ? (
            <div className={styles.stepOne}>
              <div className={styles.tabs}>
                <button
                  type="button"
                  className={`${styles.tab} ${activeTab === 'note' ? styles.tabActive : ''}`}
                  onClick={() => handleTabChange('note')}
                >
                  <HiOutlinePencilAlt /> Заметка
                </button>
                <button
                  type="button"
                  className={`${styles.tab} ${activeTab === 'animal' ? styles.tabActive : ''}`}
                  onClick={() => handleTabChange('animal')}
                >
                  <HiOutlineCamera /> Животное
                </button>
              </div>

              <div className={styles.fieldGroup}>
                <label>Заголовок</label>
                <input
                  name="title"
                  value={formData.title}
                  onChange={handleChange}
                  placeholder="О чем ваш пост?"
                  required
                />
              </div>

              {activeTab === 'animal' && (
                <div className={styles.animalFields}>
                  <div className={styles.fieldGroup}>
                    <label>Название животного</label>
                    <input
                      name="animalName"
                      value={formData.animalName}
                      onChange={handleChange}
                      placeholder="Напр: Снежный барс"
                      required={!isEdit}
                    />
                  </div>
                  <div className={styles.fieldGroup}>
                    <label>Тип (Таксон)</label>
                    <select
                      name="taxon"
                      value={formData.taxon}
                      onChange={handleChange}
                      className={styles.selectInput}
                    >
                      {TAXON_OPTIONS.map(opt => (
                        <option key={opt.value} value={opt.value}>{opt.label}</option>
                      ))}
                    </select>
                  </div>
                  <div className={styles.fieldGroup}>
                    <label>Научное название</label>
                    <input
                      name="scientificName"
                      value={formData.scientificName}
                      onChange={handleChange}
                      placeholder="Panthera uncia"
                    />
                  </div>
                </div>
              )}

              <div className={styles.fieldGroup}>
                <label>Описание</label>
                <textarea
                  name="content"
                  value={formData.content}
                  onChange={handleChange}
                  placeholder="Поделитесь подробностями..."
                  rows="4"
                  required
                />
              </div>

              {isEdit ? (
                <>
                  <div className={styles.fieldGroup}>
                    <label><HiOutlinePhotograph /> Ссылка на фото</label>
                    <input
                      name="imageUrl"
                      value={formData.imageUrl}
                      onChange={handleChange}
                      placeholder="https://example.com/image.jpg"
                    />
                  </div>
                  <div className={styles.fieldGroup}>
                    <label><HiOutlineLocationMarker /> Местоположение</label>
                    <input
                      name="location"
                      value={formData.location}
                      onChange={handleChange}
                      placeholder="Где это было?"
                    />
                  </div>
                  <div className={styles.fieldGroup}>
                    <label>Теги</label>
                    <input
                      name="tags"
                      value={formData.tags}
                      onChange={handleChange}
                      placeholder="лес, горы (через запятую)"
                    />
                  </div>
                  <div className={styles.actions}>
                    <button type="button" className={styles.secondaryBtn} onClick={handleClose}>
                      Отмена
                    </button>
                    <button type="submit" className={styles.primaryBtn} disabled={loading}>
                      {loading ? 'Сохранение...' : 'Сохранить'}
                    </button>
                  </div>
                </>
              ) : (
                <button
                  type="button"
                  className={styles.primaryBtn}
                  onClick={() => setStep(2)}
                  disabled={!formData.title || !formData.content}
                >
                  Далее
                </button>
              )}
            </div>
          ) : (
            <div className={styles.stepTwo}>
              <div className={styles.fieldGroup}>
                <label><HiOutlinePhotograph /> Ссылка на фото</label>
                <input
                  name="imageUrl"
                  value={formData.imageUrl}
                  onChange={handleChange}
                  placeholder="https://example.com/image.jpg"
                />
              </div>
              <div className={styles.fieldGroup}>
                <label><HiOutlineLocationMarker /> Местоположение</label>
                <input
                  name="location"
                  value={formData.location}
                  onChange={handleChange}
                  placeholder="Где это было?"
                />
              </div>
              <div className={styles.fieldGroup}>
                <label>Теги</label>
                <input
                  name="tags"
                  value={formData.tags}
                  onChange={handleChange}
                  placeholder="лес, горы (через запятую)"
                />
              </div>
              <div className={styles.actions}>
                <button type="button" className={styles.secondaryBtn} onClick={() => setStep(1)}>
                  Назад
                </button>
                <button type="submit" className={styles.primaryBtn} disabled={loading}>
                  {loading ? 'Публикация...' : 'Опубликовать'}
                </button>
              </div>
            </div>
          )}
        </form>
      </div>
    </div>
  );
};