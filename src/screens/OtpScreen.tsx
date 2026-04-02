import React, { useState } from 'react';
import { View, Text, TextInput, TouchableOpacity, StyleSheet } from 'react-native';
import AsyncStorage from '@react-native-async-storage/async-storage';

export default function OtpScreen({ route, navigation, setIsLoggedIn }: any) {
  const { phone } = route.params;
  const [otp, setOtp] = useState('');

  const handleVerify = async () => {
    // TODO: Replace with backend API
    // const response = await axios.post('/verify-otp', { phone, otp });

    if (otp === '1234') { // mock OTP
      const user = { phone };
      await AsyncStorage.setItem('user', JSON.stringify(user));
      setIsLoggedIn(true);
    } else {
      alert('Invalid OTP');
    }
  };

  return (
    <View style={styles.container}>
      <Text style={styles.title}>Verify OTP</Text>
      <Text style={styles.subtitle}>Sent to {phone}</Text>

      <TextInput
        placeholder="Enter OTP"
        style={styles.input}
        keyboardType="number-pad"
        value={otp}
        onChangeText={setOtp}
      />

      <TouchableOpacity style={styles.button} onPress={handleVerify}>
        <Text style={styles.buttonText}>Verify</Text>
      </TouchableOpacity>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    justifyContent: 'center',
    padding: 20,
    backgroundColor: '#0B0F1A',
  },
  title: {
    fontSize: 26,
    color: '#fff',
    marginBottom: 10,
  },
  subtitle: {
    color: '#aaa',
    marginBottom: 20,
  },
  input: {
    backgroundColor: '#1C2230',
    color: '#fff',
    padding: 15,
    borderRadius: 10,
    marginBottom: 15,
  },
  button: {
    backgroundColor: '#4CAF50',
    padding: 15,
    borderRadius: 10,
    alignItems: 'center',
  },
  buttonText: {
    color: '#fff',
    fontSize: 16,
  },
});