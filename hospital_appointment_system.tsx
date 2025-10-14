import React, { useState } from 'react';
import { Calendar, Clock, User, Mail, Phone, Search, Plus, Edit2, Trash2, CheckCircle, XCircle, Users, Activity } from 'lucide-react';

const initialDoctors = [
  { id: 1, name: 'Dr. Sarah Johnson', specialty: 'Cardiology', email: 'sarah.j@hospital.com', phone: '(555) 123-4567' },
  { id: 2, name: 'Dr. Michael Chen', specialty: 'Neurology', email: 'michael.c@hospital.com', phone: '(555) 234-5678' },
  { id: 3, name: 'Dr. Emily Brown', specialty: 'Pediatrics', email: 'emily.b@hospital.com', phone: '(555) 345-6789' }
];

const initialAppointments = [
  { id: 1, patientName: 'John Doe', email: 'john@email.com', phone: '(555) 111-2222', doctorId: 1, date: '2025-10-20', time: '10:00', status: 'confirmed', reason: 'Regular checkup' },
  { id: 2, patientName: 'Jane Smith', email: 'jane@email.com', phone: '(555) 222-3333', doctorId: 2, date: '2025-10-21', time: '14:00', status: 'pending', reason: 'Consultation' }
];

const timeSlots = ['09:00', '10:00', '11:00', '14:00', '15:00', '16:00', '17:00'];

export default function HospitalAppointmentSystem() {
  const [view, setView] = useState('patient');
  const [doctors, setDoctors] = useState(initialDoctors);
  const [appointments, setAppointments] = useState(initialAppointments);
  const [searchTerm, setSearchTerm] = useState('');
  
  const [bookingForm, setBookingForm] = useState({
    patientName: '', email: '', phone: '', doctorId: '', date: '', time: '', reason: ''
  });
  
  const [doctorForm, setDoctorForm] = useState({ name: '', specialty: '', email: '', phone: '' });
  const [editingDoctor, setEditingDoctor] = useState(null);
  const [showDoctorForm, setShowDoctorForm] = useState(false);

  const handleBookAppointment = () => {
    if (!bookingForm.patientName || !bookingForm.email || !bookingForm.phone || !bookingForm.doctorId || !bookingForm.date || !bookingForm.time || !bookingForm.reason) {
      alert('Please fill in all fields');
      return;
    }
    
    const newAppointment = {
      id: appointments.length + 1,
      ...bookingForm,
      doctorId: parseInt(bookingForm.doctorId),
      status: 'pending'
    };
    setAppointments([...appointments, newAppointment]);
    setBookingForm({ patientName: '', email: '', phone: '', doctorId: '', date: '', time: '', reason: '' });
    alert('Appointment booked successfully! You will receive a confirmation message.');
  };

  const handleAddDoctor = () => {
    if (!doctorForm.name || !doctorForm.specialty || !doctorForm.email || !doctorForm.phone) {
      alert('Please fill in all fields');
      return;
    }
    
    if (editingDoctor) {
      setDoctors(doctors.map(d => d.id === editingDoctor.id ? { ...doctorForm, id: d.id } : d));
      setEditingDoctor(null);
    } else {
      setDoctors([...doctors, { ...doctorForm, id: doctors.length + 1 }]);
    }
    setDoctorForm({ name: '', specialty: '', email: '', phone: '' });
    setShowDoctorForm(false);
  };

  const handleEditDoctor = (doctor) => {
    setDoctorForm(doctor);
    setEditingDoctor(doctor);
    setShowDoctorForm(true);
  };

  const handleDeleteDoctor = (id) => {
    if (confirm('Are you sure you want to delete this doctor?')) {
      setDoctors(doctors.filter(d => d.id !== id));
    }
  };

  const updateAppointmentStatus = (id, status) => {
    setAppointments(appointments.map(apt => apt.id === id ? { ...apt, status } : apt));
  };

  const deleteAppointment = (id) => {
    if (confirm('Are you sure you want to delete this appointment?')) {
      setAppointments(appointments.filter(apt => apt.id !== id));
    }
  };

  const filteredAppointments = appointments.filter(apt => {
    const doctor = doctors.find(d => d.id === apt.doctorId);
    return apt.patientName.toLowerCase().includes(searchTerm.toLowerCase()) ||
           doctor?.name.toLowerCase().includes(searchTerm.toLowerCase());
  });

  const getDoctorName = (doctorId) => {
    return doctors.find(d => d.id === doctorId)?.name || 'Unknown';
  };

  const stats = {
    totalAppointments: appointments.length,
    confirmed: appointments.filter(a => a.status === 'confirmed').length,
    pending: appointments.filter(a => a.status === 'pending').length,
    totalDoctors: doctors.length
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100">
      <div className="bg-white shadow-md">
        <div className="max-w-7xl mx-auto px-4 py-6">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-3">
              <div className="bg-indigo-600 p-3 rounded-lg">
                <Activity className="text-white" size={32} />
              </div>
              <div>
                <h1 className="text-3xl font-bold text-gray-900">MedCare Hospital</h1>
                <p className="text-gray-600">Appointment Management System</p>
              </div>
            </div>
            <div className="flex gap-2">
              <button
                onClick={() => setView('patient')}
                className={`px-6 py-2 rounded-lg font-medium transition ${
                  view === 'patient' ? 'bg-indigo-600 text-white' : 'bg-gray-200 text-gray-700 hover:bg-gray-300'
                }`}
              >
                Patient Portal
              </button>
              <button
                onClick={() => setView('admin')}
                className={`px-6 py-2 rounded-lg font-medium transition ${
                  view === 'admin' ? 'bg-indigo-600 text-white' : 'bg-gray-200 text-gray-700 hover:bg-gray-300'
                }`}
              >
                Admin Panel
              </button>
            </div>
          </div>
        </div>
      </div>

      <div className="max-w-7xl mx-auto px-4 py-8">
        {view === 'patient' ? (
          <div className="grid md:grid-cols-2 gap-8">
            <div className="bg-white rounded-xl shadow-lg p-6">
              <h2 className="text-2xl font-bold text-gray-900 mb-6 flex items-center gap-2">
                <Calendar className="text-indigo-600" />
                Book an Appointment
              </h2>
              <div className="space-y-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">Full Name</label>
                  <input
                    type="text"
                    value={bookingForm.patientName}
                    onChange={(e) => setBookingForm({ ...bookingForm, patientName: e.target.value })}
                    className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-transparent"
                    placeholder="John Doe"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">Email</label>
                  <input
                    type="email"
                    value={bookingForm.email}
                    onChange={(e) => setBookingForm({ ...bookingForm, email: e.target.value })}
                    className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-transparent"
                    placeholder="john@email.com"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">Phone</label>
                  <input
                    type="tel"
                    value={bookingForm.phone}
                    onChange={(e) => setBookingForm({ ...bookingForm, phone: e.target.value })}
                    className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-transparent"
                    placeholder="(555) 123-4567"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">Select Doctor</label>
                  <select
                    value={bookingForm.doctorId}
                    onChange={(e) => setBookingForm({ ...bookingForm, doctorId: e.target.value })}
                    className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-transparent"
                  >
                    <option value="">Choose a doctor</option>
                    {doctors.map(doctor => (
                      <option key={doctor.id} value={doctor.id}>
                        {doctor.name} - {doctor.specialty}
                      </option>
                    ))}
                  </select>
                </div>
                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">Date</label>
                    <input
                      type="date"
                      value={bookingForm.date}
                      onChange={(e) => setBookingForm({ ...bookingForm, date: e.target.value })}
                      min={new Date().toISOString().split('T')[0]}
                      className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-transparent"
                    />
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">Time</label>
                    <select
                      value={bookingForm.time}
                      onChange={(e) => setBookingForm({ ...bookingForm, time: e.target.value })}
                      className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-transparent"
                    >
                      <option value="">Select time</option>
                      {timeSlots.map(slot => (
                        <option key={slot} value={slot}>{slot}</option>
                      ))}
                    </select>
                  </div>
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">Reason for Visit</label>
                  <textarea
                    value={bookingForm.reason}
                    onChange={(e) => setBookingForm({ ...bookingForm, reason: e.target.value })}
                    className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-transparent"
                    rows="3"
                    placeholder="Brief description of your symptoms or reason for visit"
                  />
                </div>
                <button
                  onClick={handleBookAppointment}
                  className="w-full bg-indigo-600 text-white py-3 rounded-lg font-medium hover:bg-indigo-700 transition flex items-center justify-center gap-2"
                >
                  <CheckCircle size={20} />
                  Book Appointment
                </button>
              </div>
            </div>

            <div className="bg-white rounded-xl shadow-lg p-6">
              <h2 className="text-2xl font-bold text-gray-900 mb-6 flex items-center gap-2">
                <Users className="text-indigo-600" />
                Available Doctors
              </h2>
              <div className="space-y-4">
                {doctors.map(doctor => (
                  <div key={doctor.id} className="border border-gray-200 rounded-lg p-4 hover:shadow-md transition">
                    <div className="flex items-start gap-3">
                      <div className="bg-indigo-100 p-3 rounded-full">
                        <User className="text-indigo-600" size={24} />
                      </div>
                      <div className="flex-1">
                        <h3 className="font-bold text-lg text-gray-900">{doctor.name}</h3>
                        <p className="text-indigo-600 font-medium">{doctor.specialty}</p>
                        <div className="mt-2 space-y-1 text-sm text-gray-600">
                          <div className="flex items-center gap-2">
                            <Mail size={16} />
                            {doctor.email}
                          </div>
                          <div className="flex items-center gap-2">
                            <Phone size={16} />
                            {doctor.phone}
                          </div>
                        </div>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </div>
        ) : (
          <div>
            <div className="grid md:grid-cols-4 gap-6 mb-8">
              <div className="bg-white rounded-lg shadow p-6">
                <div className="flex items-center justify-between">
                  <div>
                    <p className="text-gray-600 text-sm">Total Appointments</p>
                    <p className="text-3xl font-bold text-gray-900">{stats.totalAppointments}</p>
                  </div>
                  <Calendar className="text-indigo-600" size={40} />
                </div>
              </div>
              <div className="bg-white rounded-lg shadow p-6">
                <div className="flex items-center justify-between">
                  <div>
                    <p className="text-gray-600 text-sm">Confirmed</p>
                    <p className="text-3xl font-bold text-green-600">{stats.confirmed}</p>
                  </div>
                  <CheckCircle className="text-green-600" size={40} />
                </div>
              </div>
              <div className="bg-white rounded-lg shadow p-6">
                <div className="flex items-center justify-between">
                  <div>
                    <p className="text-gray-600 text-sm">Pending</p>
                    <p className="text-3xl font-bold text-yellow-600">{stats.pending}</p>
                  </div>
                  <Clock className="text-yellow-600" size={40} />
                </div>
              </div>
              <div className="bg-white rounded-lg shadow p-6">
                <div className="flex items-center justify-between">
                  <div>
                    <p className="text-gray-600 text-sm">Total Doctors</p>
                    <p className="text-3xl font-bold text-purple-600">{stats.totalDoctors}</p>
                  </div>
                  <Users className="text-purple-600" size={40} />
                </div>
              </div>
            </div>

            <div className="bg-white rounded-xl shadow-lg p-6 mb-8">
              <div className="flex justify-between items-center mb-6">
                <h2 className="text-2xl font-bold text-gray-900">Manage Doctors</h2>
                <button
                  onClick={() => {
                    setShowDoctorForm(!showDoctorForm);
                    setEditingDoctor(null);
                    setDoctorForm({ name: '', specialty: '', email: '', phone: '' });
                  }}
                  className="bg-indigo-600 text-white px-4 py-2 rounded-lg hover:bg-indigo-700 transition flex items-center gap-2"
                >
                  <Plus size={20} />
                  Add Doctor
                </button>
              </div>

              {showDoctorForm && (
                <div className="bg-gray-50 p-4 rounded-lg mb-6">
                  <div className="grid md:grid-cols-2 gap-4">
                    <input
                      type="text"
                      value={doctorForm.name}
                      onChange={(e) => setDoctorForm({ ...doctorForm, name: e.target.value })}
                      placeholder="Doctor Name"
                      className="px-4 py-2 border border-gray-300 rounded-lg"
                    />
                    <input
                      type="text"
                      value={doctorForm.specialty}
                      onChange={(e) => setDoctorForm({ ...doctorForm, specialty: e.target.value })}
                      placeholder="Specialty"
                      className="px-4 py-2 border border-gray-300 rounded-lg"
                    />
                    <input
                      type="email"
                      value={doctorForm.email}
                      onChange={(e) => setDoctorForm({ ...doctorForm, email: e.target.value })}
                      placeholder="Email"
                      className="px-4 py-2 border border-gray-300 rounded-lg"
                    />
                    <input
                      type="tel"
                      value={doctorForm.phone}
                      onChange={(e) => setDoctorForm({ ...doctorForm, phone: e.target.value })}
                      placeholder="Phone"
                      className="px-4 py-2 border border-gray-300 rounded-lg"
                    />
                  </div>
                  <div className="flex gap-2 mt-4">
                    <button onClick={handleAddDoctor} className="bg-green-600 text-white px-4 py-2 rounded-lg hover:bg-green-700">
                      {editingDoctor ? 'Update' : 'Add'} Doctor
                    </button>
                    <button
                      onClick={() => setShowDoctorForm(false)}
                      className="bg-gray-400 text-white px-4 py-2 rounded-lg hover:bg-gray-500"
                    >
                      Cancel
                    </button>
                  </div>
                </div>
              )}

              <div className="space-y-3">
                {doctors.map(doctor => (
                  <div key={doctor.id} className="flex items-center justify-between p-4 border border-gray-200 rounded-lg">
                    <div>
                      <h3 className="font-bold text-gray-900">{doctor.name}</h3>
                      <p className="text-sm text-gray-600">{doctor.specialty} • {doctor.email}</p>
                    </div>
                    <div className="flex gap-2">
                      <button
                        onClick={() => handleEditDoctor(doctor)}
                        className="p-2 text-blue-600 hover:bg-blue-50 rounded-lg"
                      >
                        <Edit2 size={18} />
                      </button>
                      <button
                        onClick={() => handleDeleteDoctor(doctor.id)}
                        className="p-2 text-red-600 hover:bg-red-50 rounded-lg"
                      >
                        <Trash2 size={18} />
                      </button>
                    </div>
                  </div>
                ))}
              </div>
            </div>

            <div className="bg-white rounded-xl shadow-lg p-6">
              <div className="flex justify-between items-center mb-6">
                <h2 className="text-2xl font-bold text-gray-900">Manage Appointments</h2>
                <div className="relative">
                  <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400" size={20} />
                  <input
                    type="text"
                    placeholder="Search appointments..."
                    value={searchTerm}
                    onChange={(e) => setSearchTerm(e.target.value)}
                    className="pl-10 pr-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500"
                  />
                </div>
              </div>

              <div className="overflow-x-auto">
                <table className="w-full">
                  <thead className="bg-gray-50">
                    <tr>
                      <th className="px-4 py-3 text-left text-sm font-semibold text-gray-900">Patient</th>
                      <th className="px-4 py-3 text-left text-sm font-semibold text-gray-900">Doctor</th>
                      <th className="px-4 py-3 text-left text-sm font-semibold text-gray-900">Date & Time</th>
                      <th className="px-4 py-3 text-left text-sm font-semibold text-gray-900">Reason</th>
                      <th className="px-4 py-3 text-left text-sm font-semibold text-gray-900">Status</th>
                      <th className="px-4 py-3 text-left text-sm font-semibold text-gray-900">Actions</th>
                    </tr>
                  </thead>
                  <tbody className="divide-y divide-gray-200">
                    {filteredAppointments.map(apt => (
                      <tr key={apt.id} className="hover:bg-gray-50">
                        <td className="px-4 py-3">
                          <div>
                            <div className="font-medium text-gray-900">{apt.patientName}</div>
                            <div className="text-sm text-gray-600">{apt.email}</div>
                          </div>
                        </td>
                        <td className="px-4 py-3 text-sm text-gray-900">{getDoctorName(apt.doctorId)}</td>
                        <td className="px-4 py-3 text-sm text-gray-900">
                          {apt.date} at {apt.time}
                        </td>
                        <td className="px-4 py-3 text-sm text-gray-600">{apt.reason}</td>
                        <td className="px-4 py-3">
                          <span className={`px-3 py-1 rounded-full text-xs font-medium ${
                            apt.status === 'confirmed' ? 'bg-green-100 text-green-800' :
                            apt.status === 'pending' ? 'bg-yellow-100 text-yellow-800' :
                            'bg-red-100 text-red-800'
                          }`}>
                            {apt.status}
                          </span>
                        </td>
                        <td className="px-4 py-3">
                          <div className="flex gap-2">
                            {apt.status === 'pending' && (
                              <button
                                onClick={() => updateAppointmentStatus(apt.id, 'confirmed')}
                                className="p-1 text-green-600 hover:bg-green-50 rounded"
                                title="Confirm"
                              >
                                <CheckCircle size={18} />
                              </button>
                            )}
                            {apt.status === 'confirmed' && (
                              <button
                                onClick={() => updateAppointmentStatus(apt.id, 'cancelled')}
                                className="p-1 text-red-600 hover:bg-red-50 rounded"
                                title="Cancel"
                              >
                                <XCircle size={18} />
                              </button>
                            )}
                            <button
                              onClick={() => deleteAppointment(apt.id)}
                              className="p-1 text-red-600 hover:bg-red-50 rounded"
                              title="Delete"
                            >
                              <Trash2 size={18} />
                            </button>
                          </div>
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}