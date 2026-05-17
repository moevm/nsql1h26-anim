import { useState, useRef } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { FaUser, FaSignOutAlt, FaDownload, FaUpload } from 'react-icons/fa';
import { useAuth } from '@contexts/index';
import { Avatar } from '@components/ui/avatar';
import { Dropdown } from '@components/ui/dropdown';
import styles from './Header.module.css';
import { request } from '@api/axios';

const MAX_FILE_BYTES = 100 * 1024 * 1024;

export const Header = () => {
  const { logout, user } = useAuth();
  const navigate = useNavigate();
  const fileInputRef = useRef(null);

  const [importState, setImportState] = useState(null); 
  const [importError, setImportError] = useState('');
  const [exportLoading, setExportLoading] = useState(false);

  const handleLogout = async () => {
    await logout();
    navigate('/login');
  };

  const handleExport = async () => {
    if (exportLoading) return;

    setExportLoading(true);
    try {
      const blob = await request('get', 'system/export', null, {
        responseType: 'blob',
      });

      const url = URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = `db_export_${Date.now()}.json`;
      a.click();
      URL.revokeObjectURL(url);
    } catch {
      alert('Ошибка при экспорте базы данных');
    } finally {
      setExportLoading(false);
    }
  };

  const handleImportClick = () => {
    fileInputRef.current?.click();
    setImportState(null);
    setImportError('');
  };

  const handleFileChange = async (e) => {
    const file = e.target.files?.[0];
    e.target.value = '';

    if (!file) return;

    if (!file.name.toLowerCase().endsWith('.json')) {
      setImportError('Файл должен иметь расширение .json');
      setImportState('error');
      setTimeout(() => setImportState(null), 3000);
      return;
    }
    if (file.size === 0) {
      setImportError('Файл пустой');
      setImportState('error');
      setTimeout(() => setImportState(null), 3000);
      return;
    }
    if (file.size > MAX_FILE_BYTES) {
      setImportError('Файл слишком большой (максимум 100 МБ)');
      setImportState('error');
      setTimeout(() => setImportState(null), 3000);
      return;
    }

    try {
      const text = await file.text();
      const json = JSON.parse(text);
      if (!Array.isArray(json.nodes) || !Array.isArray(json.relationships)) {
        throw new Error('Отсутствуют поля nodes / relationships');
      }
    } catch (err) {
      setImportError(`Неверная структура файла: ${err.message}`);
      setImportState('error');
      setTimeout(() => setImportState(null), 3000);
      return;
    }

    const confirmed = window.confirm(
      'Импорт полностью заменит текущую базу данных. Продолжить?'
    );
    if (!confirmed) return;

    setImportState('loading');
    setImportError('');

    const formData = new FormData();
    formData.append('file', file);

    try {
      await request('post', 'system/import', formData, {
        headers: { 'Content-Type': 'multipart/form-data' },
      });
      setImportState('success');
      setTimeout(() => setImportState(null), 3000);
    } catch (err) {
      const msg =
        err?.response?.data?.detail ||
        err?.response?.data?.error?.message ||
        'Ошибка при импорте';
      setImportError(msg);
      setImportState('error');
      setTimeout(() => setImportState(null), 3000);
    }
  };

  const renderToast = () => {
    if (!importState) return null;
    if (importState === 'loading')
      return <div className={styles.toast}>Импорт…</div>;
    if (importState === 'success')
      return (
        <div className={`${styles.toast} ${styles.toastSuccess}`}>
          База данных успешно импортирована ✓
        </div>
      );
    if (importState === 'error')
      return (
        <div className={`${styles.toast} ${styles.toastError}`}>
          {importError}
        </div>
      );
    return null;
  };

  const menuItems = [
    { to: '/profile', label: 'Мой профиль', icon: <FaUser /> },
    {
      label: exportLoading ? 'Экспорт…' : 'Экспорт БД',
      icon: <FaDownload />,
      onClick: handleExport,
    },
    { label: 'Импорт БД', icon: <FaUpload />, onClick: handleImportClick },
    { label: 'Выйти', icon: <FaSignOutAlt />, onClick: handleLogout },
  ];

  return (
    <>
      <input
        ref={fileInputRef}
        type="file"
        accept=".json,application/json"
        style={{ display: 'none' }}
        onChange={handleFileChange}
      />

      {renderToast()}

      <header className={styles.headerExternal}>
        <div className={styles.headerInternal}>
          <div className={styles.headerContent}>

            <div className={styles.logoArea} onClick={() => navigate('/')}>
              <h1>WildLife</h1>
            </div>

            <nav className={styles.navLinks}>
              <Link to="/feed" className={styles.navItem}>Лента</Link>
              <Link to="/stats" className={styles.navItem}>Статистика</Link>
              <Link to="/profile" className={styles.navItem}>Профиль</Link>
            </nav>

            <div className={styles.userActions}>
              <Dropdown
                trigger={
                  <>
                    <Avatar size={34} />
                    <span className={styles.userName}>{user?.username}</span>
                  </>
                }
                items={menuItems}
                position="bottom"
              />
            </div>

          </div>
        </div>
      </header>
    </>
  );
};