import React, { useState } from 'react';
import { View, Text, StyleSheet, TouchableOpacity, ScrollView } from 'react-native';

export default function ClaimsScreen() {
  const [logs, setLogs] = useState<any[]>([]);
  const [completed, setCompleted] = useState(false);

  const simulateAlert = async () => {
    setLogs([]);
    setCompleted(false);

    // =========================
    // TODO: CONNECT BACKEND
    // =========================
    // const res = await axios.post('/simulate-alert');
    // setLogs(res.data.logs);
    // setCompleted(true);

    // =========================
    // MOCK FLOW (Step-by-step)
    // =========================
    const steps = [
      { title: 'IMD Red Alert Detected', desc: 'Rainfall > 80mm/hr in South Delhi' },
      { title: 'NDMA SACHET Confirmed', desc: 'Flood alert — Lajpat Nagar district' },
      { title: 'Policyholder Located', desc: 'Raju Verma — GS-3847 — Standard Plan' },
      { title: 'GPS Check Running', desc: 'Verifying inactivity...' },
      { title: 'Mock Location Check', desc: 'No spoofing detected' },
      { title: 'Accelerometer Verified', desc: 'No movement — valid claim' },
      { title: 'Fraud Checks Passed', desc: 'All validations successful' },
      { title: 'Payout ₹785 Initiated', desc: 'Processing transfer...' },
    ];

    for (let i = 0; i < steps.length; i++) {
      await new Promise((res) => setTimeout(res, 700));
      setLogs((prev) => [...prev, steps[i]]);
    }

    setCompleted(true);
  };

  return (
    <ScrollView style={styles.container}>
      
      {/* Button */}
      <TouchableOpacity style={styles.button} onPress={simulateAlert}>
        <Text style={styles.buttonText}>🌧️ Simulate Flood Alert</Text>
      </TouchableOpacity>

      {/* Logs */}
      {logs.map((log, index) => (
        <View key={index} style={styles.logCard}>
          <View>
            <Text style={styles.logTitle}>{log.title}</Text>
            <Text style={styles.logDesc}>{log.desc}</Text>
          </View>
          <Text style={styles.tick}>✔</Text>
        </View>
      ))}

      {/* Final Result */}
      {completed && (
        <View style={styles.resultCard}>
          <Text style={styles.resultTitle}>AMOUNT TRANSFERRED</Text>
          <Text style={styles.amount}>₹785</Text>
          <Text style={styles.subText}>→ raju.verma@okaxis</Text>

          <View style={styles.resultRow}>
            <Text style={styles.label}>Trigger</Text>
            <Text style={styles.value}>IMD Red Alert — Flood</Text>
          </View>

          <View style={styles.resultRow}>
            <Text style={styles.label}>Zone</Text>
            <Text style={styles.value}>Lajpat Nagar</Text>
          </View>

          <View style={styles.resultRow}>
            <Text style={styles.label}>Fraud Check</Text>
            <Text style={styles.success}>✔ Passed</Text>
          </View>

          <TouchableOpacity style={styles.doneBtn}>
            <Text style={{ color: '#fff' }}>Done</Text>
          </TouchableOpacity>
        </View>
      )}

    </ScrollView>
  );
}
const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#0B0F1A',
    padding: 20,
  },

  button: {
    backgroundColor: '#E53935',
    padding: 15,
    borderRadius: 15,
    alignItems: 'center',
    marginBottom: 20,
  },

  buttonText: {
    color: '#fff',
    fontWeight: 'bold',
  },

  logCard: {
    backgroundColor: '#1C2230',
    padding: 15,
    borderRadius: 15,
    marginBottom: 10,
    flexDirection: 'row',
    justifyContent: 'space-between',
  },

  logTitle: {
    color: '#fff',
    fontWeight: 'bold',
  },

  logDesc: {
    color: '#aaa',
  },

  tick: {
    color: '#00E6A8',
    fontSize: 18,
  },

  resultCard: {
    backgroundColor: '#1E7C7C',
    padding: 20,
    borderRadius: 20,
    marginTop: 20,
  },

  resultTitle: {
    color: '#A0E7E5',
    textAlign: 'center',
  },

  amount: {
    color: '#fff',
    fontSize: 40,
    fontWeight: 'bold',
    textAlign: 'center',
  },

  subText: {
    color: '#CFFFEF',
    textAlign: 'center',
    marginBottom: 20,
  },

  resultRow: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    marginBottom: 10,
  },

  label: {
    color: '#ccc',
  },

  value: {
    color: '#fff',
  },

  success: {
    color: '#00E6A8',
  },

  doneBtn: {
    backgroundColor: '#0B0F1A',
    padding: 15,
    borderRadius: 10,
    alignItems: 'center',
    marginTop: 20,
  },
});