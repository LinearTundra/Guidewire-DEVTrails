import React from 'react';
import { View, StyleSheet } from 'react-native';

export default function CustomCard({ children }: any) {
  return <View style={styles.card}>{children}</View>;
}

const styles = StyleSheet.create({
  card: {
    backgroundColor: '#1C2230',
    padding: 20,
    borderRadius: 16,
    marginBottom: 15,

    // Shadow (for premium look)
    shadowColor: '#000',
    shadowOpacity: 0.3,
    shadowRadius: 10,
    elevation: 5,
  },
});