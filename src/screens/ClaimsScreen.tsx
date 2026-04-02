import React, { useEffect, useState } from 'react';
import { View, Text, StyleSheet } from 'react-native';

export default function ClaimsScreen() {
  const [claims, setClaims] = useState([]);

  useEffect(() => {
    fetchClaims();
  }, []);

  const fetchClaims = async () => {
    try {
      // TODO: API INTEGRATION
      // const response = await axios.get('/claims');

      const mockData = [
        { id: 1, amount: 300, status: 'Paid' },
      ];

      setClaims(mockData);
    } catch (error) {
      console.log(error);
    }
  };

  return (
    <View style={styles.container}>
      <Text style={styles.title}>Claims</Text>

      {claims.map((c: any) => (
        <View key={c.id} style={styles.card}>
          <Text style={styles.text}>Amount: ₹{c.amount}</Text>
          <Text style={styles.text}>Status: {c.status}</Text>
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