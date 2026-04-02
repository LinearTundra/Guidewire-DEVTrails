import React, { useEffect, useState } from 'react';
import { View, Text, StyleSheet } from 'react-native';

export default function ProfileScreen() {
  const [user, setUser] = useState<any>(null);

  useEffect(() => {
    fetchProfile();
  }, []);

  const fetchProfile = async () => {
    try {
      // TODO: API INTEGRATION
      // const response = await axios.get('/user/profile');

      const mockUser = {
        name: 'Nitik',
        phone: '9999999999',
      };

      setUser(mockUser);
    } catch (error) {
      console.log(error);
    }
  };

  return (
    <View style={styles.container}>
      <Text style={styles.title}>Profile</Text>

      <View style={styles.card}>
        <Text style={styles.text}>Name: {user?.name}</Text>
        <Text style={styles.text}>Phone: {user?.phone}</Text>
      </View>
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: '#0B0F1A', padding: 20 },
  title: { color: '#fff', fontSize: 22, marginBottom: 20 },
  card: {
    backgroundColor: '#1C2230',
    padding: 15,
    borderRadius: 10,
  },
  text: { color: '#fff' },
});