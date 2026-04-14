import { Link } from 'react-router-dom'

const container = {
  display: 'flex',
  flexDirection: 'row',
  justifyContent: 'center',
  gap: '4px',
  fontSize: '14px'
}

const linkStyle = {
  color: 'var(--accent-color)',
  textDecoration: 'none',
  fontWeight: '500'
}

const question = {
  color: '#aaa'
}

export const AuthFooter = ({
  title,
  link,
  to
}) => {
  return (
    <div style={container}>
      <span style={question}>{title}</span>
      <Link to={to} style={linkStyle}>
        {link}
      </Link>
    </div>
  );
}