import React, { useState } from 'react';
import { View, Text, TouchableOpacity, StyleSheet, Modal } from 'react-native';
import AsyncStorage from '@react-native-async-storage/async-storage';
import { Ionicons } from '@expo/vector-icons';

export default function Header({ setIsLoggedIn }: any) {
  const [modalVisible, setModalVisible] = useState(false);

  const handleLogout = async () => {
    await AsyncStorage.removeItem('user');
    setIsLoggedIn(false);
  };

  return (
    <View style={styles.container}>
      <Text style={styles.logo}>GigShield</Text>

      <TouchableOpacity onPress={() => setModalVisible(true)}>
        <View style={styles.profileIcon}>
          <Ionicons name="person-circle-outline" size={32} color="#fff" />
        </View>
      </TouchableOpacity>

      {/* Profile Modal */}
      <Modal visible={modalVisible} transparent animationType="fade">
        <TouchableOpacity
          style={styles.modalOverlay}
          onPress={() => setModalVisible(false)}
        >
          <View style={styles.modalContent}>
            
            {/* TODO: Fetch user profile from backend */}
            {/* Example:
                const response = await axios.get('/user/profile');
            */}

            <Text style={styles.menuItem}>Profile</Text>

            <TouchableOpacity onPress={handleLogout}>
              <Text style={styles.menuItem}>Logout</Text>
            </TouchableOpacity>

          </View>
        </TouchableOpacity>
      </Modal>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    height: 70,
    backgroundColor: '#0B0F1A',
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    paddingHorizontal: 20,
  },
  logo: {
    color: '#fff',
    fontSize: 20,
    fontWeight: 'bold',
  },
  profileIcon: {
    width: 35,
    height: 35,
    borderRadius: 20,
    backgroundColor: '#1C2230',
    justifyContent: 'center',
    alignItems: 'center',
  },
  modalOverlay: {
    flex: 1,
    backgroundColor: 'rgba(0,0,0,0.5)',
    justifyContent: 'flex-start',
    alignItems: 'flex-end',
    paddingTop: 70,
    paddingRight: 20,
  },
  modalContent: {
    backgroundColor: '#1C2230',
    borderRadius: 10,
    padding: 15,
    width: 150,
  },
  menuItem: {
    color: '#fff',
    paddingVertical: 10,
  },
});