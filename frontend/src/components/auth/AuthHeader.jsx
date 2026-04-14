const headerWrapper = {
  display: 'flex',
  flexDirection: 'column',
  alignItems: 'center',
  gap: '12px',
  width: '100%'
}

const headerLogoContainer = {
  display: 'flex',
  alignItems: 'center',
  justifyContent: 'center',
  width: '64px',
  height: '64px',
  backgroundColor: '#eef4f0',
  border: '2px solid var(--accent-color)',
  borderRadius: '12px'
}

const headerLogo = {
  width: '32px',
  height: '32px',
  color: 'var(--accent-color)',
  objectFit: 'cover',
  objectPosition: 'center'
}

const headerTitle = {
  fontSize: '28px',
  color: '#1a1a1a',
  fontWeight: 700
}

const headerDescription = {
  fontSize: '14px',
  color: '#aaa',
  textAlign: 'center'
}

export const AuthHeader = ({
  icon: Icon,
  title,
  description
}) => {
  return (
    <div style={headerWrapper}>
      <div style={headerLogoContainer}>
        {Icon && <Icon style={headerLogo} />}
      </div>
      {title && <h1 style={headerTitle}>{title}</h1>}
      {description && <span style={headerDescription}>{description}</span>}
    </div>
  );
}