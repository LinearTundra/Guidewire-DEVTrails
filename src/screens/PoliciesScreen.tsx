import React, { useEffect, useState } from 'react';
import { View, Text, StyleSheet } from 'react-native';

export default function PoliciesScreen() {
  const [policies, setPolicies] = useState([]);

  useEffect(() => {
    fetchPolicies();
  }, []);

  const fetchPolicies = async () => {
    try {
      // TODO: API INTEGRATION
      // const response = await axios.get('/policies');
      
      const mockData = [
        { id: 1, premium: 50, status: 'Active' },
      ];

      setPolicies(mockData);
    } catch (error) {
      console.log(error);
    }
  };

  return (
    <View style={styles.container}>
      <Text style={styles.title}>Policies</Text>

      {policies.map((p: any) => (
        <View key={p.id} style={styles.card}>
          <Text style={styles.text}>Premium: ₹{p.premium}</Text>
          <Text style={styles.text}>Status: {p.status}</Text>
        </View>
      ))}
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
    marginBottom: 10,
  },
  text: { color: '#fff' },
});