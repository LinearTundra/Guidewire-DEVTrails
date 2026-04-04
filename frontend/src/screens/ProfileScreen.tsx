import React, { useState } from 'react';
import {
  View,
  Text,
  StyleSheet,
  TextInput,
  TouchableOpacity,
  ScrollView,
} from 'react-native';
import { SafeAreaView } from 'react-native-safe-area-context';

export default function ProfileScreen() {
  const [name, setName] = useState('Raju Verma');
  const [aadhaar, setAadhaar] = useState('XXXX - XXXX - 4521');
  const [platform, setPlatform] = useState('Swiggy + Zomato');
  const [zone, setZone] = useState('Lajpat Nagar');
  const [plan, setPlan] = useState('Standard');
  const [upi, setUpi] = useState('raju.verma@okaxis');

  const zones = ['Lajpat Nagar', 'Karol Bagh', 'Dwarka', 'Saket', 'Rohini'];

  const handleSubmit = async () => {
    try {
      // =========================
      // TODO: CONNECT BACKEND
      // =========================
      // await axios.post('/create-profile', {
      //   name,
      //   aadhaar,
      //   platform,
      //   zone,
      //   plan,
      //   upi,
      // });

      console.log('Profile Submitted:', {
        name,
        aadhaar,
        platform,
        zone,
        plan,
        upi,
      });

      alert('Profile Activated ✅');
    } catch (err) {
      console.log(err);
    }
  };

  return (
  <SafeAreaView style={styles.container}>
    <ScrollView contentContainerStyle={{ padding: 20 }}>
      
      <Text style={styles.title}>Get Covered</Text>
      <Text style={styles.subtitle}>
        Complete your profile to activate GigShield
      </Text>

      {/* Name */}
      <Text style={styles.label}>FULL NAME</Text>
      <TextInput
        style={styles.input}
        value={name}
        onChangeText={setName}
      />

      {/* Aadhaar */}
      <Text style={styles.label}>AADHAAR NUMBER (MASKED)</Text>
      <TextInput
        style={styles.input}
        value={aadhaar}
        onChangeText={setAadhaar}
      />

      {/* Platform */}
      <Text style={styles.label}>DELIVERY PLATFORM</Text>
      <TextInput
        style={styles.input}
        value={platform}
        onChangeText={setPlatform}
      />

      {/* Zones */}
      <Text style={styles.label}>SELECT OPERATING ZONE</Text>
      <View style={styles.zoneContainer}>
        {zones.map((z) => (
          <TouchableOpacity
            key={z}
            style={[
              styles.zoneBtn,
              zone === z && styles.zoneActive,
            ]}
            onPress={() => setZone(z)}
          >
            <Text style={{ color: '#fff' }}>{z}</Text>
          </TouchableOpacity>
        ))}
      </View>

      {/* Plans */}
      <Text style={styles.label}>CHOOSE YOUR PLAN</Text>

      {[ 
        { name: 'Basic', price: 25 },
        { name: 'Standard', price: 38 },
        { name: 'Premium', price: 55 },
      ].map((p) => (
        <TouchableOpacity
          key={p.name}
          style={[
            styles.planCard,
            plan === p.name && styles.planActive,
          ]}
          onPress={() => setPlan(p.name)}
        >
          <View>
            <Text style={styles.planName}>{p.name}</Text>
            <Text style={styles.planDesc}>Coverage plan</Text>
          </View>

          <Text style={styles.price}>₹{p.price}</Text>
        </TouchableOpacity>
      ))}

      {/* UPI */}
      <Text style={styles.label}>UPI ID</Text>
      <TextInput
        style={styles.input}
        value={upi}
        onChangeText={setUpi}
      />

      {/* Submit */}
      <TouchableOpacity style={styles.button} onPress={handleSubmit}>
        <Text style={styles.buttonText}>Activate Coverage →</Text>
      </TouchableOpacity>

    </ScrollView>
  </SafeAreaView>
);
}
const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#0B0F1A',
  },

  title: {
    color: '#fff',
    fontSize: 26,
    fontWeight: 'bold',
  },

  subtitle: {
    color: '#aaa',
    marginBottom: 20,
  },

  label: {
    color: '#aaa',
    marginTop: 15,
    marginBottom: 5,
  },

  input: {
    backgroundColor: '#1C2230',
    padding: 15,
    borderRadius: 12,
    color: '#fff',
  },

  zoneContainer: {
    flexDirection: 'row',
    flexWrap: 'wrap',
  },

  zoneBtn: {
    borderWidth: 1,
    borderColor: '#333',
    padding: 10,
    borderRadius: 20,
    margin: 5,
  },

  zoneActive: {
    backgroundColor: '#1E7C7C',
  },

  planCard: {
    backgroundColor: '#1C2230',
    padding: 15,
    borderRadius: 15,
    marginTop: 10,
    flexDirection: 'row',
    justifyContent: 'space-between',
  },

  planActive: {
    borderColor: '#FF8C42',
    borderWidth: 2,
  },

  planName: {
    color: '#fff',
    fontWeight: 'bold',
  },

  planDesc: {
    color: '#aaa',
  },

  price: {
    color: '#FF8C42',
    fontWeight: 'bold',
  },

  button: {
    backgroundColor: '#1E7C7C',
    padding: 18,
    borderRadius: 15,
    alignItems: 'center',
    marginTop: 25,
  },

  buttonText: {
    color: '#fff',
    fontWeight: 'bold',
  },
});