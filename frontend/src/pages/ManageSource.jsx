import React, { useState, useEffect } from 'react'
import { Link } from 'react-router-dom'
import { 
  ArrowLeft, 
  Search, 
  Filter, 
  ChevronUp, 
  ChevronDown, 
  Trash2, 
  Eye,
  Check,
  Square,
  Database,
  RefreshCw
} from 'lucide-react'
import { Button } from '../components/ui/button'
import { toast } from '../hooks/use-toast'

// Table configuration for different data sources
const TABLE_CONFIGS = {
  InspectionData: {
    name: 'Inspection Data',
    columns: [
      { key: 'ID', label: 'ID', type: 'number' },
      { key: 'Inspection_ID', label: 'Inspection ID', type: 'number' },
      { key: 'Machine_Type', label: 'Machine Type', type: 'string' },
      { key: 'Model_Code', label: 'Model Code', type: 'string' },
      { key: 'Serial_No', label: 'Serial Number', type: 'string' },
      { key: 'Inspected_By', label: 'Inspector', type: 'string' },
      { key: 'Equipment_Number', label: 'Equipment Number', type: 'string' },
      { key: 'SMR', label: 'SMR Hours', type: 'number' },
      { key: 'Delivery_Date', label: 'Delivery Date', type: 'date' },
      { key: 'Inspection_Date', label: 'Inspection Date', type: 'date' },
      { key: 'Branch_Name', label: 'Branch', type: 'string' },
      { key: 'Customer_Name', label: 'Customer', type: 'string' },
      { key: 'Job_Site', label: 'Job Site', type: 'string' },
      { key: 'WorkingHourPerDay', label: 'Working Hours/Day', type: 'number' },
      { key: 'UnderfootConditions_Terrain', label: 'Terrain', type: 'string' },
      { key: 'UnderfootConditions_Abrasive', label: 'Abrasive Level', type: 'string' },
      { key: 'Link_Type', label: 'Link Type', type: 'string' },
      { key: 'Link_Spec', label: 'Link Specification', type: 'string' },
      { key: 'Bushing_Spec', label: 'Bushing Spec', type: 'string' },
      { key: 'Track_Roller_Spec', label: 'Track Roller Spec', type: 'string' },
      { key: 'ApplicationCode_Major', label: 'Application Major', type: 'string' },
      { key: 'ApplicationCode_Minor', label: 'Application Minor', type: 'string' },
      { key: 'Attachments', label: 'Attachments', type: 'string' },
      { key: 'Comments', label: 'Comments', type: 'string' }
    ]
  },
  Machine_Tracking: {
    name: 'Machine Tracking', 
    columns: [
      { key: 'ID', label: 'ID', type: 'number' },
      { key: 'Model', label: 'Model', type: 'string' },
      { key: 'Type', label: 'Type', type: 'string' },
      { key: 'Serial', label: 'Serial Number', type: 'string' },
      { key: 'Delivery_Date_EQP_Care', label: 'Delivery Date', type: 'date' },
      { key: 'Machine_Location', label: 'Machine Location', type: 'string' },
      { key: 'Latitude', label: 'Latitude', type: 'number' },
      { key: 'Longitude', label: 'Longitude', type: 'number' },
      { key: 'GPS_Time', label: 'GPS Time', type: 'datetime' },
      { key: 'SMR_Hours', label: 'SMR Hours', type: 'number' },
      { key: 'Last_Communication_Date', label: 'Last Communication', type: 'datetime' }
    ]
  },
  UC_Life_Time: {
    name: 'UC Life Time',
    columns: [
      { key: 'ID', label: 'ID', type: 'number' },
      { key: 'Model', label: 'Model', type: 'string' },
      { key: 'General_Sand', label: 'General Sand', type: 'string' },
      { key: 'Soil', label: 'Soil', type: 'string' },
      { key: 'Marsh', label: 'Marsh', type: 'string' },
      { key: 'Coal', label: 'Coal', type: 'string' },
      { key: 'Hard_Rock', label: 'Hard Rock', type: 'string' },
      { key: 'Brittle_Rock', label: 'Brittle Rock', type: 'string' },
      { key: 'Pure_Sand_Middle_East', label: 'Pure Sand Middle East', type: 'string' },
      { key: 'Component', label: 'Component', type: 'string' }
    ]
  }
}

const ManageSource = () => {
  const [selectedTable, setSelectedTable] = useState('InspectionData')
  const [tableData, setTableData] = useState([])
  const [filteredData, setFilteredData] = useState([])
  const [loading, setLoading] = useState(true)
  const [selectedRows, setSelectedRows] = useState(new Set())
  const [searchTerm, setSearchTerm] = useState('')
  const [sortConfig, setSortConfig] = useState({ key: null, direction: 'asc' })
  const [showDeleteConfirm, setShowDeleteConfirm] = useState(false)
  const [currentPage, setCurrentPage] = useState(1)
  const [rowsPerPage, setRowsPerPage] = useState(25)

  useEffect(() => {
    loadTableData()
  }, [selectedTable])

  useEffect(() => {
    filterAndSortData()
  }, [tableData, searchTerm, sortConfig])

  useEffect(() => {
    setCurrentPage(1) // Reset to first page when filter changes
  }, [filteredData])

  const loadTableData = async () => {
    try {
      setLoading(true)
      setSelectedRows(new Set())
      
      // Try to fetch real data from database first
      try {
        const query = `SELECT TOP 1000 * FROM ${selectedTable}`
        console.log('🔍 Fetching data from:', '/database/query', 'for table:', selectedTable, '(limit: 1000 rows)', new Date().toISOString())
        const response = await fetch('/database/query', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            query: query,
            system_type: 'UMS'
          })
        })

        console.log('📡 Response status:', response.status, response.ok)
        if (response.ok) {
          const result = await response.json()
          console.log('✅ API Response:', { 
            success: result.success, 
            dataLength: result.data?.length, 
            totalRecords: result.total_records,
            tableName: selectedTable,
            message: result.message 
          })
          if (result.success && result.data && result.data.length > 0) {
            console.log('🎯 Setting tableData with', result.data.length, 'records')
            setTableData(result.data)
            toast.success(`✅ REAL DATA: Loaded ${result.data.length} records from ${TABLE_CONFIGS[selectedTable].name}`)
            return
          } else {
            console.warn('❌ API returned empty or invalid data:', result)
          }
        } else {
          console.warn('❌ API response not ok:', response.status, response.statusText)
        }
      } catch (apiError) {
        console.warn('❌ API request failed, falling back to sample data:', apiError)
      }
      
      // Fallback to sample data if API fails
      console.log('⚠️ Using sample data fallback for table:', selectedTable)
      const sampleData = generateSampleData(selectedTable)
      console.log('📊 Generated sample data:', sampleData.length, 'records')
      setTableData(sampleData)
      toast.info(`⚠️ SAMPLE DATA: Showing ${sampleData.length} fake records for ${TABLE_CONFIGS[selectedTable].name}`)
      
    } catch (error) {
      console.error('Error loading table data:', error)
      toast.error(`Failed to load ${TABLE_CONFIGS[selectedTable].name} data: ${error.message}`)
      setTableData([])
    } finally {
      setLoading(false)
    }
  }

  const generateSampleData = (tableName) => {
    // Generate realistic sample data for demo purposes
    const sampleSize = 1000
    const data = []
    
    // Sample data templates for each table
    const sampleTemplates = {
      InspectionData: {
        machines: ['PC200-8', 'PC350-8', 'D65PX-18', 'WA380-8', 'GD555-6'],
        branches: ['Jakarta', 'Balikpapan', 'Surabaya', 'Bandung', 'Palembang'],
        customers: ['PT Adaro', 'PT Bukit Asam', 'PT Vale', 'PT Antam', 'PT Pertamina'],
        inspectors: ['John Doe', 'Jane Smith', 'Ahmad Rizki', 'Siti Nurhaliza', 'Budi Santoso'],
        terrain: ['Rocky', 'Sandy', 'Muddy', 'Normal', 'Extreme'],
        abrasive: ['Low', 'Medium', 'High', 'Very High']
      },
      Machine_Tracking: {
        models: ['PC200-8', 'PC350-8', 'D65PX-18', 'WA380-8', 'GD555-6'],
        types: ['Excavator', 'Bulldozer', 'Wheel Loader', 'Dump Truck', 'Motor Grader'],
        locations: ['Jakarta Site', 'Balikpapan Mine', 'Surabaya Port', 'Bandung Quarry', 'Palembang Plant'],
        coordinates: [
          { lat: -6.2088, lng: 106.8456 }, // Jakarta
          { lat: -1.2379, lng: 116.8529 }, // Balikpapan
          { lat: -7.2575, lng: 112.7521 }, // Surabaya
          { lat: -6.9175, lng: 107.6191 }, // Bandung
          { lat: -2.9761, lng: 104.7754 }  // Palembang
        ]
      },
      UC_Life_Time: {
        models: ['PC200-8', 'PC350-8', 'D65PX-18', 'WA380-8', 'GD555-6'],
        components: ['Track Chain', 'Sprocket', 'Idler', 'Track Roller', 'Drive Motor', 'Final Drive'],
        terrainValues: ['Low', 'Medium', 'High', 'Very High', 'Extreme']
      }
    }
    
    const template = sampleTemplates[tableName]
    
    for (let i = 1; i <= sampleSize; i++) {
      const row = {}
      
      TABLE_CONFIGS[tableName].columns.forEach(column => {
        switch (column.key) {
          // Common ID fields
          case 'ID':
            row[column.key] = i
            break
          case 'Inspection_ID':
            row[column.key] = 119550 + i
            break
          case 'Machine_ID':
          case 'Component_ID':
            row[column.key] = `${tableName.substring(0,3).toUpperCase()}${String(i).padStart(4, '0')}`
            break
            
          // InspectionData specific
          case 'Machine_Type':
          case 'Model_Code':
          case 'Model':
            row[column.key] = template?.machines?.[Math.floor(Math.random() * template.machines.length)] || `Model-${i}`
            break
          case 'Serial_No':
          case 'Serial_Number':
            row[column.key] = `SN${String(Math.floor(Math.random() * 900000) + 100000)}`
            break
          case 'Inspected_By':
            row[column.key] = template?.inspectors?.[Math.floor(Math.random() * template.inspectors.length)] || `Inspector ${i}`
            break
          case 'Branch_Name':
            row[column.key] = template?.branches?.[Math.floor(Math.random() * template.branches.length)] || `Branch ${i}`
            break
          case 'Customer_Name':
            row[column.key] = template?.customers?.[Math.floor(Math.random() * template.customers.length)] || `Customer ${i}`
            break
          case 'Equipment_Number':
            row[column.key] = `EX-${String(i).padStart(4, '0')}`
            break
          case 'Job_Site':
            row[column.key] = `Job Site ${String.fromCharCode(65 + (i % 26))}`
            break
          case 'UnderfootConditions_Terrain':
            row[column.key] = template?.terrain?.[Math.floor(Math.random() * template.terrain.length)] || 'Normal'
            break
          case 'UnderfootConditions_Abrasive':
            row[column.key] = template?.abrasive?.[Math.floor(Math.random() * template.abrasive.length)] || 'Medium'
            break
            
          // Machine_Tracking specific  
          case 'Type':
            row[column.key] = template?.types?.[Math.floor(Math.random() * template.types.length)] || `Type ${i}`
            break
          case 'Serial':
            row[column.key] = `SN${String(Math.floor(Math.random() * 900000) + 100000)}`
            break
          case 'Delivery_Date_EQP_Care':
            row[column.key] = new Date(Date.now() - Math.random() * 365 * 3 * 24 * 60 * 60 * 1000).toISOString().split('T')[0]
            break
          case 'Machine_Location':
            row[column.key] = template?.locations?.[Math.floor(Math.random() * template.locations.length)] || `Location ${i}`
            break
          case 'Latitude':
            const coordIndex = Math.floor(Math.random() * (template?.coordinates?.length || 5))
            row[column.key] = template?.coordinates?.[coordIndex]?.lat || (-6 + Math.random() * 5)
            break
          case 'Longitude':
            const coordIndex2 = Math.floor(Math.random() * (template?.coordinates?.length || 5))
            row[column.key] = template?.coordinates?.[coordIndex2]?.lng || (104 + Math.random() * 10)
            break
          case 'GPS_Time':
          case 'Last_Communication_Date':
            row[column.key] = new Date(Date.now() - Math.random() * 7 * 24 * 60 * 60 * 1000).toISOString()
            break
            
          // UC_Life_Time specific
          case 'General_Sand':
          case 'Soil':
          case 'Marsh':
          case 'Coal':
          case 'Hard_Rock':
          case 'Brittle_Rock':
          case 'Pure_Sand_Middle_East':
            row[column.key] = template?.terrainValues?.[Math.floor(Math.random() * template.terrainValues.length)] || 'Medium'
            break
          case 'Component':
            row[column.key] = template?.components?.[Math.floor(Math.random() * template.components.length)] || `Component ${i}`
            break
            
          // Number fields
          case 'SMR':
          case 'SMR_Hours':
          case 'Current_Hours':
            row[column.key] = Math.floor(Math.random() * 50000) + 1000
            break
          case 'WorkingHourPerDay':
            row[column.key] = Math.floor(Math.random() * 16) + 8
            break
          case 'Expected_Life_Hours':
            row[column.key] = Math.floor(Math.random() * 20000) + 10000
            break
          case 'Remaining_Life_Hours':
            row[column.key] = Math.floor(Math.random() * 15000) + 1000
            break
            
          // Date fields
          case 'Delivery_Date':
          case 'Installation_Date':
            row[column.key] = new Date(Date.now() - Math.random() * 365 * 2 * 24 * 60 * 60 * 1000).toISOString().split('T')[0]
            break
          case 'Inspection_Date':
          case 'Last_Maintenance_Date':
            row[column.key] = new Date(Date.now() - Math.random() * 30 * 24 * 60 * 60 * 1000).toISOString().split('T')[0]
            break
          case 'Last_Updated':
            row[column.key] = new Date(Date.now() - Math.random() * 7 * 24 * 60 * 60 * 1000).toISOString()
            break
            
          default:
            row[column.key] = `Sample ${i}`
        }
      })
      data.push(row)
    }
    
    return data
  }

  const filterAndSortData = () => {
    let filtered = [...tableData]

    // Apply search filter across all columns
    if (searchTerm) {
      const currentConfig = TABLE_CONFIGS[selectedTable]
      filtered = filtered.filter(row =>
        currentConfig.columns.some(col => {
          const value = row[col.key]
          if (value === null || value === undefined) return false
          return value.toString().toLowerCase().includes(searchTerm.toLowerCase())
        })
      )
    }

    // Apply sorting
    if (sortConfig.key) {
      filtered.sort((a, b) => {
        let aValue = a[sortConfig.key]
        let bValue = b[sortConfig.key]

        // Handle null/undefined values
        if (aValue === null || aValue === undefined) aValue = ''
        if (bValue === null || bValue === undefined) bValue = ''

        // Handle different data types
        const columnConfig = TABLE_CONFIGS[selectedTable].columns.find(col => col.key === sortConfig.key)
        if (columnConfig?.type === 'number') {
          aValue = parseFloat(aValue) || 0
          bValue = parseFloat(bValue) || 0
        } else if (columnConfig?.type === 'date' || columnConfig?.type === 'datetime') {
          aValue = new Date(aValue).getTime() || 0
          bValue = new Date(bValue).getTime() || 0
        } else {
          aValue = aValue.toString().toLowerCase()
          bValue = bValue.toString().toLowerCase()
        }

        if (aValue < bValue) {
          return sortConfig.direction === 'asc' ? -1 : 1
        }
        if (aValue > bValue) {
          return sortConfig.direction === 'asc' ? 1 : -1
        }
        return 0
      })
    }

    setFilteredData(filtered)
  }

  const handleSort = (key) => {
    let direction = 'asc'
    if (sortConfig.key === key && sortConfig.direction === 'asc') {
      direction = 'desc'
    }
    setSortConfig({ key, direction })
  }

  const handleSelectRow = (id) => {
    const newSelected = new Set(selectedRows)
    if (newSelected.has(id)) {
      newSelected.delete(id)
    } else {
      newSelected.add(id)
    }
    setSelectedRows(newSelected)
  }

  const handleSelectAll = () => {
    const currentPageData = getPaginatedData()
    const currentPageIds = currentPageData.map(row => getRowId(row))
    
    if (selectedRows.size === currentPageIds.length && currentPageIds.every(id => selectedRows.has(id))) {
      // Deselect all current page items
      const newSelected = new Set(selectedRows)
      currentPageIds.forEach(id => newSelected.delete(id))
      setSelectedRows(newSelected)
    } else {
      // Select all current page items
      const newSelected = new Set(selectedRows)
      currentPageIds.forEach(id => newSelected.add(id))
      setSelectedRows(newSelected)
    }
  }

  const getRowId = (row) => {
    // Use ID field if available, otherwise use first column value
    return row.ID || row[TABLE_CONFIGS[selectedTable].columns[0].key] || Math.random()
  }

  const handleDeleteSelected = async () => {
    if (selectedRows.size === 0) {
      toast.error('No rows selected')
      return
    }

    try {
      // For now, we'll show a message that delete is not implemented for database tables
      toast.info('Delete functionality for database tables will be implemented based on business requirements')
      setShowDeleteConfirm(false)
      setSelectedRows(new Set())
    } catch (error) {
      console.error('Error deleting rows:', error)
      toast.error('Delete Failed')
    } finally {
      setShowDeleteConfirm(false)
    }
  }

  const getPaginatedData = () => {
    const startIndex = (currentPage - 1) * rowsPerPage
    const endIndex = startIndex + rowsPerPage
    return filteredData.slice(startIndex, endIndex)
  }

  const totalPages = Math.ceil(filteredData.length / rowsPerPage)

  const formatValue = (value, type) => {
    if (value === null || value === undefined) return '-'
    
    switch (type) {
      case 'date':
        return new Date(value).toLocaleDateString()
      case 'datetime':
        return new Date(value).toLocaleString()
      case 'number':
        return typeof value === 'number' ? value.toLocaleString() : value
      default:
        return value.toString()
    }
  }

  const handleTableChange = (tableName) => {
    setSelectedTable(tableName)
    setSearchTerm('')
    setSortConfig({ key: null, direction: 'asc' })
    setCurrentPage(1)
  }

  const getSortIcon = (key) => {
    if (sortConfig.key !== key) {
      return <ChevronUp className="h-4 w-4 text-gray-400" />
    }
    return sortConfig.direction === 'asc' 
      ? <ChevronUp className="h-4 w-4 text-blue-600" />
      : <ChevronDown className="h-4 w-4 text-blue-600" />
  }

  const currentConfig = TABLE_CONFIGS[selectedTable]

  if (loading) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 p-4 sm:p-8">
        <div className="max-w-7xl mx-auto">
          <div className="bg-white rounded-lg shadow-xl p-4 sm:p-8">
            <div className="text-center">
              <RefreshCw className="h-8 w-8 animate-spin mx-auto mb-4 text-blue-600" />
              <div>Loading {currentConfig.name}...</div>
            </div>
          </div>
        </div>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 p-4 sm:p-8">
      <div className="max-w-7xl mx-auto">
        <div className="bg-white rounded-lg shadow-xl p-4 sm:p-8">
          {/* Header */}
          <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between mb-6 gap-4">
            <div className="flex flex-col sm:flex-row items-start sm:items-center gap-4">
              <Link to="/">
                <Button variant="outline" className="gap-2">
                  <ArrowLeft className="h-4 w-4" />
                  Back to Home
                </Button>
              </Link>
              <div>
                <h1 className="text-2xl sm:text-3xl font-bold text-gray-900">Database Management</h1>
                <p className="text-sm text-gray-600 mt-1">Viewing: {currentConfig.name}</p>
              </div>
            </div>
            <div className="flex items-center gap-4">
              <div className="text-sm text-gray-600">
                Total Records: {filteredData.length}
              </div>
              <Button onClick={loadTableData} variant="outline" className="gap-2">
                <RefreshCw className="h-4 w-4" />
                Refresh
              </Button>
            </div>
          </div>

          {/* Table Selector */}
          <div className="mb-6">
            <div className="flex flex-col sm:flex-row gap-4">
              <div className="flex items-center gap-2">
                <Database className="h-5 w-5 text-gray-600" />
                <span className="text-sm font-medium text-gray-700">Select Table:</span>
              </div>
              <div className="flex flex-wrap gap-2">
                {Object.keys(TABLE_CONFIGS).map((tableName) => (
                  <button
                    key={tableName}
                    onClick={() => handleTableChange(tableName)}
                    className={`px-4 py-2 rounded-lg text-sm font-medium transition-colors ${
                      selectedTable === tableName
                        ? 'bg-blue-600 text-white shadow-md'
                        : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
                    }`}
                  >
                    {TABLE_CONFIGS[tableName].name}
                  </button>
                ))}
              </div>
            </div>
          </div>

          {/* Filters and Search */}
          <div className="mb-6 space-y-4">
            <div className="flex flex-col sm:flex-row gap-4 items-start sm:items-center">
              <div className="flex items-center gap-2 flex-1">
                <Search className="h-4 w-4 text-gray-500" />
                <input
                  type="text"
                  placeholder="Search across all columns..."
                  value={searchTerm}
                  onChange={(e) => setSearchTerm(e.target.value)}
                  className="flex-1 px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                />
              </div>
              
              <div className="flex items-center gap-2">
                <span className="text-sm text-gray-600">Rows per page:</span>
                <select
                  value={rowsPerPage}
                  onChange={(e) => {
                    setRowsPerPage(Number(e.target.value))
                    setCurrentPage(1)
                  }}
                  className="px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                >
                  <option value={10}>10</option>
                  <option value={25}>25</option>
                  <option value={50}>50</option>
                  <option value={100}>100</option>
                  <option value={200}>200</option>
                  <option value={500}>500</option>
                  <option value={1000}>1000</option>
                </select>
              </div>
            </div>

            {/* Action Buttons */}
            <div className="flex flex-col sm:flex-row gap-2 justify-between">
              <div className="flex gap-2">
                <Button
                  onClick={() => setShowDeleteConfirm(true)}
                  disabled={selectedRows.size === 0}
                  variant="outline"
                  className="gap-2"
                >
                  <Trash2 className="h-4 w-4" />
                  Selected ({selectedRows.size})
                </Button>
              </div>
              
              {/* Pagination Info */}
              <div className="text-sm text-gray-600 flex items-center">
                Showing {Math.min((currentPage - 1) * rowsPerPage + 1, filteredData.length)} to {Math.min(currentPage * rowsPerPage, filteredData.length)} of {filteredData.length} results
              </div>
            </div>
          </div>

          {/* Data Table */}
          <div className="overflow-x-auto border border-gray-200 rounded-lg">
            <table className="w-full border-collapse">
              <thead>
                <tr className="bg-gray-50">
                  <th className="border-b border-gray-200 p-3 text-left">
                    <div className="flex items-center gap-2">
                      <button
                        onClick={handleSelectAll}
                        className="p-1 hover:bg-gray-200 rounded"
                      >
                        {(() => {
                          const currentPageData = getPaginatedData()
                          const currentPageIds = currentPageData.map(row => getRowId(row))
                          const allSelected = currentPageIds.length > 0 && currentPageIds.every(id => selectedRows.has(id))
                          return allSelected
                            ? <Check className="h-4 w-4 text-blue-600" />
                            : <Square className="h-4 w-4 text-gray-500" />
                        })()}
                      </button>
                      <span className="hidden sm:inline">Select</span>
                    </div>
                  </th>
                  {currentConfig.columns.map((column) => (
                    <th key={column.key} className="border-b border-gray-200 p-3 text-left">
                      <button
                        onClick={() => handleSort(column.key)}
                        className="flex items-center gap-2 hover:text-blue-600 text-sm font-medium"
                      >
                        <span className="truncate">{column.label}</span>
                        {getSortIcon(column.key)}
                      </button>
                    </th>
                  ))}
                </tr>
              </thead>
              <tbody>
                {getPaginatedData().map((row, index) => {
                  const rowId = getRowId(row)
                  return (
                    <tr key={rowId} className="hover:bg-gray-50 border-b border-gray-100">
                      <td className="p-3">
                        <button
                          onClick={() => handleSelectRow(rowId)}
                          className="p-1 hover:bg-gray-200 rounded"
                        >
                          {selectedRows.has(rowId)
                            ? <Check className="h-4 w-4 text-blue-600" />
                            : <Square className="h-4 w-4 text-gray-500" />
                          }
                        </button>
                      </td>
                      {currentConfig.columns.map((column) => (
                        <td key={column.key} className="p-3 text-sm">
                          <div className="truncate max-w-xs" title={formatValue(row[column.key], column.type)}>
                            {formatValue(row[column.key], column.type)}
                          </div>
                        </td>
                      ))}
                    </tr>
                  )
                })}
              </tbody>
            </table>

            {filteredData.length === 0 && (
              <div className="text-center py-12 text-gray-500">
                <Database className="h-12 w-12 mx-auto mb-4 text-gray-300" />
                <div className="text-lg font-medium mb-2">No data found</div>
                <div className="text-sm">Try adjusting your search or refresh the data</div>
              </div>
            )}
          </div>

          {/* Pagination */}
          {totalPages > 1 && (
            <div className="mt-6 flex flex-col sm:flex-row items-center justify-between gap-4">
              <div className="text-sm text-gray-600">
                Page {currentPage} of {totalPages}
              </div>
              <div className="flex gap-2">
                <Button
                  onClick={() => setCurrentPage(1)}
                  disabled={currentPage === 1}
                  variant="outline"
                  size="sm"
                >
                  First
                </Button>
                <Button
                  onClick={() => setCurrentPage(currentPage - 1)}
                  disabled={currentPage === 1}
                  variant="outline"
                  size="sm"
                >
                  Previous
                </Button>
                
                {/* Page numbers */}
                {[...Array(Math.min(5, totalPages))].map((_, i) => {
                  const pageNum = Math.max(1, Math.min(currentPage - 2 + i, totalPages - 4 + i))
                  if (pageNum <= totalPages) {
                    return (
                      <Button
                        key={pageNum}
                        onClick={() => setCurrentPage(pageNum)}
                        variant={currentPage === pageNum ? "default" : "outline"}
                        size="sm"
                        className="hidden sm:inline-flex"
                      >
                        {pageNum}
                      </Button>
                    )
                  }
                  return null
                })}

                <Button
                  onClick={() => setCurrentPage(currentPage + 1)}
                  disabled={currentPage === totalPages}
                  variant="outline"
                  size="sm"
                >
                  Next
                </Button>
                <Button
                  onClick={() => setCurrentPage(totalPages)}
                  disabled={currentPage === totalPages}
                  variant="outline"
                  size="sm"
                >
                  Last
                </Button>
              </div>
            </div>
          )}
        </div>
      </div>

      {/* Delete Confirmation Modal */}
      {showDeleteConfirm && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
          <div className="bg-white rounded-lg p-6 max-w-md w-full">
            <h3 className="text-lg font-semibold mb-4">Confirm Action</h3>
            <p className="text-gray-600 mb-6">
              You have selected {selectedRows.size} row(s) from {currentConfig.name}. 
              Delete operations for database tables require careful consideration and proper business approval.
            </p>
            <div className="flex gap-3 justify-end">
              <Button
                onClick={() => setShowDeleteConfirm(false)}
                variant="outline"
              >
                Cancel
              </Button>
              <Button
                onClick={handleDeleteSelected}
                variant="outline"
              >
                OK
              </Button>
            </div>
          </div>
        </div>
      )}
    </div>
  )
}

export default ManageSource