import React, { useState } from 'react';
import { View, Text, TextInput, TouchableOpacity, StyleSheet } from 'react-native';
import AsyncStorage from '@react-native-async-storage/async-storage';

export default function SetupProfileScreen({ navigation, setIsLoggedIn }: any) {
  const [name, setName] = useState('');
  const [location, setLocation] = useState('');

  const handleSave = async () => {
    try {
      // TODO: CONNECT BACKEND
      // await axios.post('/create-profile', { name, location });

      const user = { name, location };
      await AsyncStorage.setItem('userProfile', JSON.stringify(user));

      setIsLoggedIn(true);
    } catch (error) {
      console.log(error);
    }
  };

  return (
    <View style={styles.container}>
      <Text style={styles.title}>Complete Your Profile</Text>

      <TextInput
        placeholder="Enter Name"
        style={styles.input}
        value={name}
        onChangeText={setName}
      />

      <TextInput
        placeholder="Enter Location"
        style={styles.input}
        value={location}
        onChangeText={setLocation}
      />

      <TouchableOpacity style={styles.button} onPress={handleSave}>
        <Text style={styles.buttonText}>Continue</Text>
      </TouchableOpacity>
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, justifyContent: 'center', padding: 20, backgroundColor: '#0B0F1A' },
  title: { color: '#fff', fontSize: 24, marginBottom: 20 },
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
  buttonText: { color: '#fff' },
});