import { useState } from 'react';
import styles from './Profile.module.css';
import { 
  User, 
  Edit2, 
  Save, 
  X,
  KeyRound,
  ShieldCheck
} from 'lucide-react';

const ProfilePage = ({user}) => {
  
  const [isEditing, setIsEditing] = useState(false);
  
  // Simulated initial user data
  const [userData, setUserData] = useState({
    first_name: user.first_name,
    last_name: user.last_name,
    email: user.email,
    role: user.role,
    company: user.company,
    newPassword: '',     // Only used if changing password
    currentPassword: ''  // Required to save
  });

  const [formData, setFormData] = useState(userData);

  const handleEditToggle = () => {
    if (isEditing) {
      setFormData(userData);
      setIsEditing(false);
    } 
    else {
      setIsEditing(true);
    }
  };

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSave = (e) => {
    e.preventDefault();
    
    // Validation: Current password must be entered to save
    if (!formData.currentPassword) {
      alert("Please enter your Current Password to confirm changes.");
      return;
    }

    // API Call would go here...
    console.log("Saving Profile:", formData);

    // Success Update
    setUserData({
      ...formData, 
      currentPassword: '', // Clear security fields after save
      newPassword: ''
    });
    setIsEditing(false);
  };

  return (
    <div className={styles.container}>
      
      {/* Profile Header Card */}
      <div className={styles.profileHeader}>
        <div className={styles.avatarLarge}>
          {userData.first_name[0]}{userData.last_name[0]}
        </div>
        <div className={styles.headerInfo}>
          <h2 className={styles.headerName}>{userData.first_name} {userData.last_name}</h2>
          <span className={styles.headerRole}>{userData.role}</span>
        </div>

        {/* Edit Toggle Button */}
        <button 
          className={`${styles.editBtn} ${isEditing ? styles.active : ''}`}
          onClick={handleEditToggle}
          title={isEditing ? "Cancel Editing" : "Edit Profile"}
        >
          {isEditing ? <X size={20} /> : <Edit2 size={20} />}
          <span>{isEditing ? "Cancel" : "Edit"}</span>
        </button>
      </div>

      {/* Main Form Card */}
      <form className={styles.formCard} onSubmit={handleSave}>
        <div className={styles.sectionTitle}>
          <User size={18} />
          <span>Personal Information</span>
        </div>

        <div className={styles.gridRow}>
          {/* First Name */}
          <div className={styles.inputGroup}>
            <label className={styles.label}>First Name</label>
            <input
              type="text"
              name="firstName"
              value={formData.first_name}
              onChange={handleChange}
              disabled={!isEditing}
              className={styles.input}
            />
          </div>

          {/* Last Name */}
          <div className={styles.inputGroup}>
            <label className={styles.label}>Last Name</label>
            <input
              type="text"
              name="lastName"
              value={formData.last_name}
              onChange={handleChange}
              disabled={!isEditing}
              className={styles.input}
            />
          </div>
        </div>

        <div className={styles.gridRow}>
          {/* Email */}
          <div className={styles.inputGroup}>
            <label className={styles.label}>Email Address</label>
              <input
                type="email"
                name="email"
                value={formData.email}
                onChange={handleChange}
                disabled={!isEditing}
                className={styles.input}
              />
          </div>

          {/* Company */}
          <div className={styles.inputGroup}>
            <label className={styles.label}>Company</label>
              <input
                type="text"
                name="company"
                value={formData.company}
                onChange={handleChange}
                disabled={!isEditing}
                className={styles.input}
              />
          </div>
        </div>

        <div className={styles.fullWidth}>
          {/* Role (Often Read-only in real apps, but editable here based on request) */}
          <div className={styles.inputGroup}>
            <label className={styles.label}>Role / Designation</label>
              <input
                type="text"
                name="role"
                value={formData.role}
                onChange={handleChange}
                disabled={!isEditing}
                className={styles.input}
              />
          </div>
        </div>

        {/* Security Section */}
        <div className={styles.divider}></div>
        <div className={styles.sectionTitle}>
          <ShieldCheck size={18} />
          <span>Security & Password</span>
        </div>

        <div className={styles.gridRow}>
          {/* New Password */}
          <div className={styles.inputGroup}>
            <label className={styles.label}>New Password</label>
              <input
                type="password"
                name="newPassword"
                placeholder={isEditing ? "Enter to change..." : "Set New Password"}
                value={formData.newPassword}
                onChange={handleChange}
                disabled={!isEditing}
                className={styles.input}
              />
            <span className={styles.hint}>Leave blank to keep current password</span>
          </div>
        </div>

        {/* --- Verification Section (Only visible when Editing) --- */}
        {isEditing && (
          <div className={styles.verificationBox}>
            <div className={styles.verificationHeader}>
              <KeyRound size={20} />
              <span>Confirm Changes</span>
            </div>
            <p>To save these updates, please enter your current password.</p>
            
            <input
              type="password"
              name="currentPassword"
              placeholder="Current Password (Required)"
              value={formData.currentPassword}
              onChange={handleChange}
              className={`${styles.input} ${styles.secureInput}`}
              required
            />

            <button type="submit" className={styles.saveBtn}>
              <Save size={18} />
              <span>Save Changes</span>
            </button>
          </div>
        )}

      </form>
    </div>
  );
};

export default ProfilePage;
