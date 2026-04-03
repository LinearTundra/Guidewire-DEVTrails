import React, { useEffect, useState } from 'react';
import { View, Text, StyleSheet, ScrollView } from 'react-native';

export default function PoliciesScreen() {
  const [policy, setPolicy] = useState<any>(null);
  const [triggers, setTriggers] = useState<any[]>([]);
  const [history, setHistory] = useState<any[]>([]);

  useEffect(() => {
    fetchPolicyData();
  }, []);

  const fetchPolicyData = async () => {
    try {
      // =========================
      // TODO: CONNECT BACKEND
      // =========================
      // const res = await axios.get('/policy');
      // setPolicy(res.data.policy);
      // setTriggers(res.data.triggers);
      // setHistory(res.data.history);

      // =========================
      // MOCK DATA
      // =========================
      const mockPolicy = {
        name: 'Standard Plan',
        premium: 38,
        payout: 1200,
        streak: 4,
        id: 'GS-DL-2026-003847',
      };

      const mockTriggers = [
        { title: 'Extreme Rainfall', desc: 'IMD Red Alert or > 50mm/hr', active: true },
        { title: 'Flooding', desc: 'NDMA active flood alert', active: true },
        { title: 'Severe AQI', desc: 'AQI > 300 sustained 4+ hours', active: true },
        { title: 'Strike / Curfew', desc: 'Premium plan only', active: false },
      ];

      const mockHistory = [
        { title: 'Flood — Lajpat Nagar', amount: 785 },
        { title: 'Severe AQI (412)', amount: 950 },
        { title: 'Heavy Rain — South Delhi', amount: 392 },
      ];

      setPolicy(mockPolicy);
      setTriggers(mockTriggers);
      setHistory(mockHistory);

    } catch (err) {
      console.log(err);
    }
  };

  return (
    <ScrollView style={styles.container}>
      
      {/* Header */}
      <Text style={styles.title}>My Policy</Text>
      <Text style={styles.subId}>{policy?.id}</Text>

      {/* Policy Card */}
      <View style={styles.card}>
        <Text style={styles.plan}>{policy?.name}</Text>
        <Text style={styles.policyId}>Policy ID: {policy?.id}</Text>

        <View style={styles.row}>
          <View>
            <Text style={styles.label}>Weekly Premium</Text>
            <Text style={styles.value}>₹{policy?.premium}</Text>
          </View>

          <View>
            <Text style={styles.label}>Max Payout</Text>
            <Text style={styles.value}>₹{policy?.payout}</Text>
          </View>

          <View>
            <Text style={styles.label}>Streak</Text>
            <Text style={styles.value}>{policy?.streak} weeks 🔥</Text>
          </View>
        </View>
      </View>

      {/* Triggers */}
      <Text style={styles.section}>Coverage Triggers</Text>

      {triggers.map((item, index) => (
        <View key={index} style={styles.triggerCard}>
          <View>
            <Text style={styles.triggerTitle}>{item.title}</Text>
            <Text style={styles.triggerDesc}>{item.desc}</Text>
          </View>

          <Text style={{ color: item.active ? '#00E6A8' : '#555' }}>
            {item.active ? '✔' : '—'}
          </Text>
        </View>
      ))}

      {/* History */}
      <Text style={styles.section}>Payout History</Text>

      {history.map((item, index) => (
        <View key={index} style={styles.historyCard}>
          <View>
            <Text style={styles.historyTitle}>{item.title}</Text>
            <Text style={styles.historySub}>Auto-approved</Text>
          </View>

          <Text style={styles.amount}>+₹{item.amount}</Text>
        </View>
      ))}

    </ScrollView>
  );
}
const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#0B0F1A',
    padding: 20,
  },

  title: {
    color: '#fff',
    fontSize: 24,
    fontWeight: 'bold',
  },

  subId: {
    color: '#aaa',
    marginBottom: 20,
  },

  card: {
    backgroundColor: '#1E7C7C',
    padding: 20,
    borderRadius: 20,
    marginBottom: 20,
  },

  plan: {
    color: '#fff',
    fontSize: 22,
    fontWeight: 'bold',
  },

  policyId: {
    color: '#CFFFEF',
    marginBottom: 15,
  },

  row: {
    flexDirection: 'row',
    justifyContent: 'space-between',
  },

  label: {
    color: '#ccc',
    fontSize: 12,
  },

  value: {
    color: '#fff',
    fontWeight: 'bold',
  },

  section: {
    color: '#fff',
    fontSize: 18,
    marginBottom: 10,
    marginTop: 10,
  },

  triggerCard: {
    backgroundColor: '#1C2230',
    padding: 15,
    borderRadius: 15,
    marginBottom: 10,
    flexDirection: 'row',
    justifyContent: 'space-between',
  },

  triggerTitle: {
    color: '#fff',
    fontWeight: 'bold',
  },

  triggerDesc: {
    color: '#aaa',
  },

  historyCard: {
    backgroundColor: '#1C2230',
    padding: 15,
    borderRadius: 15,
    marginBottom: 10,
    flexDirection: 'row',
    justifyContent: 'space-between',
  },

  historyTitle: {
    color: '#fff',
  },

  historySub: {
    color: '#aaa',
    fontSize: 12,
  },

  amount: {
    color: '#00E6A8',
    fontWeight: 'bold',
  },
});