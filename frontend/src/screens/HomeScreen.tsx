import React, { useEffect, useState } from 'react';
import { View, Text, StyleSheet, ScrollView } from 'react-native';
import Header from '../components/Header';
import { SafeAreaView } from 'react-native-safe-area-context';

export default function HomeScreen({ setIsLoggedIn }: any) {
  const [loading, setLoading] = useState(true);
  const [profile, setProfile] = useState<any>(null);
  const [dashboard, setDashboard] = useState<any>(null);

  useEffect(() => {
    fetchData();
  }, []);

  const fetchData = async () => {
    try {
      setLoading(true);

      // =========================
      // TODO: CONNECT BACKEND
      // =========================
      // const profileRes = await axios.get('/user/profile');
      // const dashboardRes = await axios.get('/dashboard');

      // setProfile(profileRes.data);
      // setDashboard(dashboardRes.data);

      // =========================
      // MOCK DATA
      // =========================
      const mockProfile = {
        name: 'Raju Verma',
        location: 'Lajpat Nagar, Delhi',
      };

      const mockDashboard = {
        earnings: 5500,
        premium: 38,
        payout: 1200,
        risk: 'High',
        lastPayout: 785,
        streak: 4,
      };

      setProfile(mockProfile);
      setDashboard(mockDashboard);
    } catch (error) {
      console.log(error);
    } finally {
      setLoading(false);
    }
  };

  // ✅ LOADING SCREEN (FIXED)
  if (loading) {
    return (
      <SafeAreaView style={styles.container}>
        <Header setIsLoggedIn={setIsLoggedIn} />
        <ScrollView contentContainerStyle={styles.content}>
          <Text style={{ color: '#fff' }}>Loading...</Text>
        </ScrollView>
      </SafeAreaView>
    );
  }

  // ✅ MAIN SCREEN (FIXED)
  return (
    <SafeAreaView style={styles.container}>
      <Header setIsLoggedIn={setIsLoggedIn} />

      <ScrollView contentContainerStyle={styles.content} showsVerticalScrollIndicator={false}>
        
        {/* Greeting */}
        <Text style={styles.greeting}>Hi 👋</Text>
        <Text style={styles.username}>{profile?.name}</Text>
        <Text style={styles.location}>📍 {profile?.location}</Text>

        {/* Active Policy */}
        <View style={styles.policyCard}>
          <Text style={styles.policyTitle}>ACTIVE POLICY</Text>
          <Text style={styles.planName}>Standard Plan</Text>
          <Text style={styles.policySub}>Coverage active</Text>

          <View style={styles.row}>
            <View>
              <Text style={styles.smallLabel}>Weekly Premium</Text>
              <Text style={styles.value}>₹{dashboard?.premium}</Text>
            </View>

            <View>
              <Text style={styles.smallLabel}>Max Payout</Text>
              <Text style={styles.value}>₹{dashboard?.payout}</Text>
            </View>

            <View>
              <Text style={styles.smallLabel}>Policy ID</Text>
              <Text style={styles.value}>GS-3847</Text>
            </View>
          </View>
        </View>

        {/* Risk Section */}
        <Text style={styles.sectionTitle}>Zone Safety Score</Text>

        <View style={styles.zoneCard}>
          <Text style={styles.zoneTitle}>{profile?.location}</Text>
          <Text style={styles.zoneSub}>Live risk data</Text>
          <Text style={styles.riskBadge}>{dashboard?.risk} Risk</Text>
        </View>

        {/* Alert */}
        <View style={styles.alertCard}>
          <Text style={styles.alertTitle}>⚠️ Weather Alert</Text>
          <Text style={styles.alertText}>
            Monitoring your zone. Payout triggers automatically.
          </Text>
        </View>

        {/* Weekly Stats */}
        <Text style={styles.sectionTitle}>This Week</Text>

        <View style={styles.statsRow}>
          <View style={styles.statCard}>
            <Text style={styles.value}>₹{dashboard?.earnings}</Text>
            <Text style={styles.smallLabel}>Earnings Protected</Text>
          </View>

          <View style={styles.statCard}>
            <Text style={styles.value}>₹{dashboard?.lastPayout}</Text>
            <Text style={styles.smallLabel}>Last Payout</Text>
          </View>

          <View style={styles.statCard}>
            <Text style={styles.value}>{dashboard?.streak} Wks</Text>
            <Text style={styles.smallLabel}>Active Streak</Text>
          </View>
        </View>

      </ScrollView>
    </SafeAreaView>
  );
}

// ✅ STYLES (UNCHANGED)
const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#0B0F1A',
  },
  content: {
    padding: 20,
  },

  greeting: { color: '#aaa' },

  username: {
    color: '#fff',
    fontSize: 24,
    fontWeight: 'bold',
  },

  location: {
    color: '#4FC3F7',
    marginBottom: 20,
  },

  policyCard: {
    backgroundColor: '#1E7C7C',
    padding: 20,
    borderRadius: 20,
    marginBottom: 20,
  },

  policyTitle: { color: '#A0E7E5', fontSize: 12 },

  planName: {
    color: '#fff',
    fontSize: 20,
    fontWeight: 'bold',
  },

  policySub: {
    color: '#CFFFEF',
    marginBottom: 15,
  },

  row: {
    flexDirection: 'row',
    justifyContent: 'space-between',
  },

  smallLabel: {
    color: '#ccc',
    fontSize: 12,
  },

  value: {
    color: '#fff',
    fontWeight: 'bold',
  },

  sectionTitle: {
    color: '#fff',
    fontSize: 18,
    marginBottom: 10,
  },

  zoneCard: {
    backgroundColor: '#1C2230',
    padding: 15,
    borderRadius: 15,
    marginBottom: 15,
  },

  zoneTitle: {
    color: '#fff',
    fontWeight: 'bold',
  },

  zoneSub: {
    color: '#aaa',
  },

  riskBadge: {
    color: '#ff4d4d',
    marginTop: 5,
  },

  alertCard: {
    backgroundColor: '#2A0F0F',
    padding: 15,
    borderRadius: 15,
    marginBottom: 20,
  },

  alertTitle: {
    color: '#ff4d4d',
    fontWeight: 'bold',
  },

  alertText: {
    color: '#ccc',
  },

  statsRow: {
    flexDirection: 'row',
    justifyContent: 'space-between',
  },

  statCard: {
    backgroundColor: '#1C2230',
    padding: 15,
    borderRadius: 15,
    width: '30%',
  },
});