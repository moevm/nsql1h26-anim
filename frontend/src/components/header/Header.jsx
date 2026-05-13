import { useNavigate, Link } from 'react-router-dom';
import { FaUser, FaSignOutAlt, FaDownload, FaUpload } from 'react-icons/fa';
import { useAuth } from '@contexts/index';
import { Avatar } from '@components/ui/avatar';
import { Dropdown } from '@components/ui/dropdown';
import styles from './Header.module.css';
import { request } from '@api/axios';

export const Header = () => {
  const { logout, user } = useAuth();
  const navigate = useNavigate();

  const handleLogout = async () => {
    await logout();
    navigate('/login');
  };

  const handleExport = async () => {
    await request('get', 'system/export')
  }

  const handleImport = async () => {
    await request('post', 'system/import')
  }

  const menuItems = [
    { to: '/profile', label: 'Мой профиль', icon: <FaUser /> },
    { label: 'Экспорт БД', icon: <FaDownload />, onClick: handleExport},
    { label: 'Импорт БД', icon: <FaUpload />, onClick: handleImport},
    { label: 'Выйти', icon: <FaSignOutAlt />, onClick: handleLogout }
  ];

  return (
    <header className={styles.headerExternal}>
      <div className={styles.headerInternal}>
        <div className={styles.headerContent}>

          <div className={styles.logoArea} onClick={() => navigate('/')}>
            <h1>WildLife</h1>
          </div>

          <nav className={styles.navLinks}>
            <Link to="/" className={`${styles.navItem} ${styles.active}`}>Лента</Link>
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
  );
};