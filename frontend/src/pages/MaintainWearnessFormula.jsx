import React from 'react';
import { useNavigate } from 'react-router-dom';
import { Home, Calculator, Info, AlertCircle } from 'lucide-react';
import { Button } from '../components/ui/button';

const MaintainWearnessFormula = () => {
  const navigate = useNavigate();

  const handleGoHome = () => {
    navigate('/');
  };

  return (
    <div className="p-8">
      <div className="max-w-4xl mx-auto">
        {/* Header */}
        <div className="bg-white rounded-lg shadow-xl p-8 mb-6">
          <div className="flex items-center justify-between mb-6">
            <div className="flex items-center gap-3">
              <Calculator className="h-8 w-8 text-komatsu-yellow" />
              <div>
                <h1 className="text-3xl font-bold text-gray-800">Maintain Wearness Formula</h1>
                <p className="text-gray-600">Formula untuk perhitungan tingkat keausan komponen</p>
              </div>
            </div>
            <Button 
              onClick={handleGoHome}
              className="komatsu-button gap-2"
            >
              <Home className="h-5 w-5" />
              Home
            </Button>
          </div>
        </div>

        {/* Formula Display */}
        <div className="bg-white rounded-lg shadow-xl p-8 mb-6">
          <div className="flex items-center gap-2 mb-6">
            <Info className="h-6 w-6 text-blue-500" />
            <h2 className="text-2xl font-semibold text-gray-800">Formula Wearness</h2>
          </div>

          {/* Formula Image Container */}
          <div className="bg-gray-50 border-2 border-dashed border-gray-300 rounded-lg p-8 text-center mb-6">
            <div className="flex flex-col items-center justify-center min-h-[300px]">
              <Calculator className="h-16 w-16 text-gray-400 mb-4" />
              <h3 className="text-lg font-medium text-gray-600 mb-2">Formula Wearness</h3>
              <div className="bg-white p-6 rounded-lg shadow-sm border max-w-2xl">
                <div className="text-xl font-mono text-center mb-4">
                  <div className="mb-3">
                    <strong>Wearness Rate = </strong>
                  </div>
                  <div className="border-t border-gray-300 pt-3">
                    <div className="text-lg">
                      <span className="text-blue-600">Operating Hours</span> × <span className="text-green-600">Load Factor</span> × <span className="text-purple-600">Environment Factor</span>
                    </div>
                    <div className="border-b border-gray-400 mt-2 mb-2"></div>
                    <div className="text-lg">
                      <span className="text-orange-600">Expected Life Hours</span> × <span className="text-red-600">Maintenance Factor</span>
                    </div>
                  </div>
                </div>
              </div>
              <p className="text-sm text-gray-500 mt-4">
                *Ganti dengan gambar formula yang sesuai
              </p>
            </div>
          </div>

          {/* Formula Components Description */}
          <div className="grid md:grid-cols-2 gap-6">
            <div className="bg-blue-50 p-6 rounded-lg">
              <h4 className="font-semibold text-blue-800 mb-3">Parameter Input</h4>
              <ul className="space-y-2 text-sm text-blue-700">
                <li><strong>Operating Hours:</strong> Jam operasional mesin</li>
                <li><strong>Load Factor:</strong> Faktor beban kerja (0-1)</li>
                <li><strong>Environment Factor:</strong> Faktor lingkungan kerja</li>
                <li><strong>Expected Life Hours:</strong> Estimasi umur komponen</li>
                <li><strong>Maintenance Factor:</strong> Faktor pemeliharaan</li>
              </ul>
            </div>

            <div className="bg-green-50 p-6 rounded-lg">
              <h4 className="font-semibold text-green-800 mb-3">Interpretasi Hasil</h4>
              <ul className="space-y-2 text-sm text-green-700">
                <li><strong>0 - 0.3:</strong> Kondisi baik, pemeliharaan rutin</li>
                <li><strong>0.3 - 0.7:</strong> Perlu perhatian, monitoring intensif</li>
                <li><strong>0.7 - 0.9:</strong> Kondisi kritis, jadwalkan penggantian</li>
                <li><strong>0.9 - 1.0:</strong> Segera ganti komponen</li>
                <li><strong>&gt; 1.0:</strong> Melampaui batas, risiko tinggi</li>
              </ul>
            </div>
          </div>
        </div>

        {/* Important Notes */}
        <div className="bg-amber-50 border border-amber-200 rounded-lg p-6">
          <div className="flex items-start gap-3">
            <AlertCircle className="h-6 w-6 text-amber-600 mt-1 flex-shrink-0" />
            <div>
              <h3 className="font-semibold text-amber-800 mb-2">Catatan Penting</h3>
              <ul className="text-sm text-amber-700 space-y-1">
                <li>• Formula ini digunakan untuk menghitung tingkat keausan komponen mesin</li>
                <li>• Nilai wearness rate yang tinggi menunjukkan komponen perlu segera diganti</li>
                <li>• Lakukan kalibrasi parameter sesuai dengan kondisi operasional spesifik</li>
                <li>• Konsultasikan dengan teknisi berpengalaman untuk interpretasi hasil</li>
              </ul>
            </div>
          </div>
        </div>

        {/* Action Buttons */}
        <div className="flex justify-center mt-8">
          <Button 
            onClick={handleGoHome}
            className="komatsu-button gap-2 text-lg px-8 py-3"
          >
            <Home className="h-5 w-5" />
            Kembali ke Menu Utama
          </Button>
        </div>
      </div>
    </div>
  );
};

export default MaintainWearnessFormula;