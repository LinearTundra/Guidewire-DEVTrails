import React, { useState } from 'react';
import { View, Text, TextInput, TouchableOpacity, StyleSheet } from 'react-native';

export default function LoginScreen({ navigation }: any) {
  const [phone, setPhone] = useState('');

  const handleSendOtp = async () => {
    // TODO: Call backend API
    // await axios.post('/send-otp', { phone });

    navigation.navigate('Otp', { phone });
  };

  return (
    <View style={styles.container}>
      <Text style={styles.title}>GigShield</Text>
      <Text style={styles.subtitle}>Login with your phone</Text>

      <TextInput
        placeholder="Enter Phone Number"
        style={styles.input}
        keyboardType="phone-pad"
        value={phone}
        onChangeText={setPhone}
      />

      <TouchableOpacity style={styles.button} onPress={handleSendOtp}>
        <Text style={styles.buttonText}>Send OTP</Text>
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
    fontSize: 32,
    color: '#fff',
    marginBottom: 10,
    fontWeight: 'bold',
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