import React, { useEffect, useState } from 'react';
import { View, Text, StyleSheet, ScrollView } from 'react-native';
import Header from '../components/Header';
import CustomCard from '../components/CustomCard';

const [loading, setLoading] = useState(true);
export default function HomeScreen({ setIsLoggedIn }: any) {
  const [data, setData] = useState<any>(null);

  useEffect(() => {
    fetchDashboardData();
  }, []);

  const fetchDashboardData = async () => {
  try {
    setLoading(true);

    // TODO: API INTEGRATION
    // const response = await axios.get('/dashboard');

    const mockData = {
      earnings: 12000,
      riskLevel: 'Medium',
      weeklyPremium: 50,
    };

    setData(mockData);
  } catch (error) {
    console.log(error);
  } finally {
    setLoading(false);
  }
};
if (loading) {
  return (
    <View style={styles.container}>
      <Text style={{ color: '#fff', textAlign: 'center', marginTop: 50 }}>
        Loading...
      </Text>
    </View>
  );
}

  return (
    <View style={styles.container}>
      <Header setIsLoggedIn={setIsLoggedIn} />

      <ScrollView style={styles.content}>
        <Text style={styles.heading}>Dashboard</Text>

        <CustomCard>
  <Text style={styles.cardTitle}>Weekly Earnings</Text>
  <Text style={styles.cardValue}>₹{data?.earnings}</Text>
</CustomCard>

<CustomCard>
  <Text style={styles.cardTitle}>Risk Level</Text>
  <Text style={styles.cardValue}>{data?.riskLevel}</Text>
</CustomCard>

<CustomCard>
  <Text style={styles.cardTitle}>Weekly Premium</Text>
  <Text style={styles.cardValue}>₹{data?.weeklyPremium}</Text>
</CustomCard>
      </ScrollView>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#0B0F1A',
  },
  content: {
    padding: 20,
  },
  heading: {
    color: '#fff',
    fontSize: 24,
    marginBottom: 20,
  },
  card: {
    backgroundColor: '#1C2230',
    padding: 20,
    borderRadius: 15,
    marginBottom: 15,
  },
  cardTitle: {
    color: '#aaa',
    marginBottom: 5,
  },
  cardValue: {
    color: '#fff',
    fontSize: 18,
    fontWeight: 'bold',
  },
});