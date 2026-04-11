import { useState, useEffect, useRef } from 'react';
import { useLocation } from 'react-router-dom';
import api from '../services/api';
import { Card, CardContent, CardHeader, CardTitle } from '../components/ui/card';
import { Input } from '../components/ui/input';
import { Label } from '../components/ui/label';
import { Button } from '../components/ui/button';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '../components/ui/select';
import { RadioGroup, RadioGroupItem } from '../components/ui/radio-group';
import { Separator } from '../components/ui/separator';
import { QRCodeCanvas } from 'qrcode.react';
import { Download, Printer, Save, Edit, Search, FileDown, History, UploadCloud, X } from 'lucide-react';
import { Badge } from '../components/ui/badge';
import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
  DialogFooter,
} from "../components/ui/dialog";
import { toast } from 'sonner';
import { DatePicker } from '../components/ui/date-picker';
import { Html5Qrcode } from 'html5-qrcode';
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "../components/ui/table";
import { Tabs, TabsContent, TabsList, TabsTrigger } from '../components/ui/tabs';

const TOOLS_LIST = [
  "Aerial Roller for Earthwire",
  "Articulator Joints",
  "Articulator Joints – 10T",
  "Articulator Joints – 25T",
  "Automatic Clamp for Earthwire – 7/3.66mm",
  "Automatic Clamp for Zebra Conductor",
  "Bull Dog Clamp – 18mm",
  "Chain Pulley – 10T Capacity",
  "Clipping Ladder",
  "Comealong Clamp (Bolted) for Earthwire",
  "Comealong Clamp (Bolted) for Zebra",
  "Conductor Drum Lifting Jacks (Manual)",
  "Conductor Drum Lifting Jacks (Manual) – 10T",
  "Crowbar – 32mm",
  "D-Shackles",
  "D-Shackles – 5T Cap",
  "D-Shackles – 6.5T Cap",
  "D-Shackles – 8.5T Cap",
  "D-Shackles – 9.5/10MT Cap",
  "D-Shackles – 17MT Cap",
  "Derrick Poles – 6m + 6m",
  "Dieset for Earthwire",
  "Dieset for Earthwire – Aluminium",
  "Dieset for Earthwire – Steel",
  "Dieset for Zebra Conductor – Aluminium",
  "Double Ended Socks for Conductor",
  "Double Sheave Pulley – 5T Cap",
  "Double sleeve open Pulley",
  "Dynamometer – 15T",
  "Earthwire Socks",
  "Equalizer Pulley",
  "E/W Drum Lifting Jacks (Manual)",
  "Four Sheave Pulley Block",
  "Ground Rollers",
  "Head Board Suitable for Seven Sheave Aerial Roller",
  "Hydraulic Conductor Cutter",
  "ISMC-400",
  "Marking Roller",
  "Midspan Joint Protector Sleeve",
  "One End Open Socks with Eye for Conductor",
  "Pilot Wire – 24mm",
  "Pilot Wire – 24mm – 800m",
  "Pilot Wire Bobbin",
  "Pilot Wire Connector – 24mm",
  "Pilot Wire Mounting Stand",
  "Pilot Wire Safety Clamp",
  "P.P. Rope – 22mm Dia",
  "P.P. Rope – 22mm Dia – 220m",
  "P.P. Rope – 24mm Dia",
  "P.P. Rope – 24mm Dia – 220m",
  "Sag Plate",
  "Safety Clamp – 3 Bolted",
  "Seven Sheave Aerial Roller – 660mm Dia Wheel (Nylon)",
  "Single Sheave Pulley – 5T Cap",
  "Single Sheave Pulley – 5T Cap – Open Type",
  "Single Sheave Pulley – 5T Cap – Closed Type",
  "Steel Wire Rope – 12mm (Fibre Coated)",
  "Steel Wire Rope – 18mm (Fibre Coated)",
  "Steel Wire Rope Slings – 18mm",
  "Steel Wire Rope Slings – 18mm – 1m",
  "Steel Wire Rope Slings – 18mm – 3m",
  "Steel Wire Rope Slings – 18mm – 5m",
  "Trifor – 5MT",
  "Turn Buckles – 10T Cap",
  "Turn Table E/W – 5 Ton Cap",
  "Turn Table E/W – 10 Ton Cap",
  "Walkie–Talkie",
  "Winch Machine – 5T (With Mechanical Clamp)"
];

const ToolMaster = () => {
  console.log("Rendering ToolMaster");
  const location = useLocation();
  const [activeTab, setActiveTab] = useState(location.state?.view || 'new');
  const [baseUrl, setBaseUrl] = useState(window.location.origin);
  const [savedTools, setSavedTools] = useState<any[]>([]);

  // Tab switching effect
  useEffect(() => {
    if (location.state?.view === 'saved') {
      setActiveTab('saved');
    } else if (location.state?.view === 'new') {
      setActiveTab('new');
      if (location.state?.mode === 'create') {
        // Reset for new entry
        setEditingToolId(null);
        setQrCode('');
        // Optional: reset toolData defaults here if needed
      } else if (location.state?.mode === 'edit') {
        const qrCodeToLoad = location.state?.qrCode;
        if (qrCodeToLoad) {
          handleFetchToolByQR(qrCodeToLoad);
        } else {
          setEditingToolId(null);
          setQrCode('');
          toast.info("Please Scan or Enter QR Code to Edit Tool");
        }
      }
    }
  }, [location.state]);

  useEffect(() => {
    const fetchIp = async () => {
      try {
        const res = await api.get('/system/ip');
        if (res.data.ip && res.data.ip !== 'localhost') {
          setBaseUrl(`http://${res.data.ip}:${window.location.port}`);
        }
      } catch (e) {
        console.warn("Could not fetch system IP, defaulting to origin");
      }
    };
    fetchIp();
  }, []);

  const fetchTools = async () => {
    try {
      const response = await api.get('/tools/');
      // Sort by ID descending to show newest first
      const sortedTools = response.data.sort((a: any, b: any) => b.id - a.id);
      setSavedTools(sortedTools);
    } catch (error) {
      console.error("Failed to fetch tools", error);
    }
  };

  useEffect(() => {
    fetchTools();
  }, []);

  const [toolData, setToolData] = useState({
    description: '',
    make: new Date().getFullYear().toString(),
    capacity: '',
    safeWorkingLoad: '',
    toolType: 'Erection Tools', // Default
    purchaserName: '',
    purchaserContact: '',
    supplierCode: '',
    testCertificate: '',
    jobCode: '',
    jobDescription: '',
    dateOfSupply: undefined as Date | undefined,
    lastInspectionDate: undefined as Date | undefined,
    inspectionResult: 'usable',
    usabilityPercentage: '',
    validityPeriod: '',
    subcontractorName: '',
    previousSite: '',
    currentSite: '',
    nextSite: '',
    expiryDate: undefined as Date | undefined,
  });

  const [qrCode, setQrCode] = useState('');
  const [searchTerm, setSearchTerm] = useState('');
  const [statusFilter, setStatusFilter] = useState('all');
  const [editingToolId, setEditingToolId] = useState<number | null>(null);
  const [scanning, setScanning] = useState(false);
  const [isToolSaved, setIsToolSaved] = useState(false);

  // History State
  const [historyTool, setHistoryTool] = useState<any>(null); // The tool currently being viewed
  const [historyData, setHistoryData] = useState<any[]>([]);
  const [isHistoryOpen, setIsHistoryOpen] = useState(false);
  
  // Bulk Import State
  const [isImportModalOpen, setIsImportModalOpen] = useState(false);
  const [importFile, setImportFile] = useState<File | null>(null);
  const [isUploading, setIsUploading] = useState(false);

  const [errors, setErrors] = useState<Record<string, boolean>>({});
  const fileInputRef = useRef<HTMLInputElement>(null);

  const [hoveredTool, setHoveredTool] = useState<any | null>(null);

  const filteredTools = savedTools.filter(tool => {
    const matchesSearch =
      tool.description.toLowerCase().includes(searchTerm.toLowerCase()) ||
      tool.qr_code.toLowerCase().includes(searchTerm.toLowerCase()) ||
      tool.make.toLowerCase().includes(searchTerm.toLowerCase()) ||
      tool.current_site?.toLowerCase().includes(searchTerm.toLowerCase());

    const matchesStatus = statusFilter === 'all' || tool.status === statusFilter;

    return matchesSearch && matchesStatus;
  });

  const handleInputChange = (field: string, value: string) => {
    setToolData(prev => ({ ...prev, [field]: value }));
    if (errors[field]) {
      setErrors(prev => ({ ...prev, [field]: false }));
    }
  };

  const handleDateChange = (field: string, date: Date | undefined) => {
    setToolData(prev => {
      const updates: any = { [field]: date };

      // Auto-calculate expiry date if dateOfSupply changes
      if (field === 'dateOfSupply' && date) {
        const expiry = new Date(date);
        expiry.setFullYear(date.getFullYear() + 3);
        // Ensure accurate date by handling leap years if necessary (JS Date handles this mostly)
        updates.expiryDate = expiry;
        updates.validityPeriod = '3';
      }

      return { ...prev, ...updates };
    });
    if (errors[field]) {
      setErrors(prev => ({ ...prev, [field]: false }));
    }
  };

  const handleCertUpload = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (file) {
      const formData = new FormData();
      formData.append('file', file);
      try {
        const response = await api.post('/upload/certificate', formData, {
          headers: { 'Content-Type': 'multipart/form-data' }
        });
        setToolData(prev => ({ ...prev, testCertificate: response.data.url }));
        toast.success("Certificate uploaded successfully");
      } catch (error) {
        console.error("Upload failed", error);
        toast.error("Failed to upload certificate");
      }
    }
  };

  // Auto-generate Tool ID / QR Code based on fields
  useEffect(() => {
    if (!editingToolId) { // Only auto-generate for new tools
      const namePart = toolData.description ? toolData.description.substring(0, 2).toUpperCase().replace(/[^A-Z]/g, 'X') : 'XX';

      let datePart = '0000';
      if (toolData.dateOfSupply) {
        const date = new Date(toolData.dateOfSupply);
        const month = (date.getMonth() + 1).toString().padStart(2, '0');
        const year = date.getFullYear().toString().substring(2);
        datePart = `${month}${year}`;
      }

      const supplierPart = toolData.purchaserName ? toolData.purchaserName.substring(0, 2).toUpperCase().replace(/[^A-Z]/g, 'X') : 'XX';
      const codePart = toolData.supplierCode ? toolData.supplierCode.padEnd(3, '0').substring(0, 3).toUpperCase() : '000'; // Ensure 3 chars

      const generatedId = `${namePart}${datePart}${supplierPart}${codePart}`;
      setQrCode(generatedId);
    }
  }, [toolData.description, toolData.dateOfSupply, toolData.purchaserName, toolData.supplierCode]);

  const validateForm = () => {
    const newErrors: Record<string, boolean> = {};
    let isValid = true;

    const requiredFields = [
      'description', 'make', 'capacity', 'safeWorkingLoad',
      'purchaserName', 'purchaserContact', 'supplierCode',
      'jobCode', 'jobDescription'
    ];

    requiredFields.forEach(field => {
      if (!toolData[field as keyof typeof toolData]) {
        newErrors[field] = true;
        isValid = false;
      }
    });

    if (!toolData.dateOfSupply) {
      newErrors['dateOfSupply'] = true;
      isValid = false;
    }

    setErrors(newErrors);
    return isValid;
  };

  const handleSave = async () => {
    // Helper to format date as YYYY-MM-DD to avoid timezone shifts
    const formatDateForApi = (date: Date | undefined) => {
      if (!date) return undefined;
      const year = date.getFullYear();
      const month = String(date.getMonth() + 1).padStart(2, '0');
      const day = String(date.getDate()).padStart(2, '0');
      return `${year}-${month}-${day}`;
    };

    try {
      if (!validateForm()) {
        toast.error("Please fill in all required fields marked with * and highlighted in red.");
        return;
      }

      const payload = {
        ...toolData,
        purchaser_name: toolData.purchaserName,
        purchaser_contact: toolData.purchaserContact,
        supplier_code: toolData.supplierCode,
        test_certificate: toolData.testCertificate,
        date_of_supply: formatDateForApi(toolData.dateOfSupply),
        last_inspection_date: formatDateForApi(toolData.lastInspectionDate),
        inspection_result: toolData.inspectionResult,
        usability_percentage: toolData.usabilityPercentage ? parseFloat(toolData.usabilityPercentage) : null,
        validity_period: toolData.validityPeriod ? parseInt(toolData.validityPeriod) : null,
        subcontractor_name: toolData.subcontractorName,
        previous_site: toolData.previousSite,
        current_site: toolData.currentSite,
        next_site: toolData.nextSite,
        status: toolData.inspectionResult === 'not-usable' ? 'scrap' : 'usable',
        safe_working_load: toolData.safeWorkingLoad,
        qr_code: qrCode, // Use the auto-generated ID
        expiry_date: formatDateForApi(toolData.expiryDate),
        job_code: toolData.jobCode,
        job_description: toolData.jobDescription
      };


      if (editingToolId) {
        await api.patch(`/tools/${editingToolId}`, payload);
        toast.success('Tool updated successfully');
        setIsToolSaved(true);
      } else {
        await api.post('/tools', payload);
        toast.success('Tool saved to database successfully');
        setIsToolSaved(true);
        // If save is successful, set active tab to saved? No, stay to show QR code
        // Keep active tab as 'new' to show the QR code
      }

      fetchTools();
      // Switch to Inventory tab after save? Or stay here?
      // For now, reload data.
    } catch (error) {
      console.error(error);
      toast.error('Failed to save tool');
    }
  };

  const generateCombinedQRUrl = (canvas: HTMLCanvasElement, text: string) => {
    const newCanvas = document.createElement('canvas');
    const ctx = newCanvas.getContext('2d');
    if (!ctx) return canvas.toDataURL('image/png');
    
    newCanvas.width = canvas.width;
    newCanvas.height = canvas.height + 40;
    
    ctx.fillStyle = '#FFFFFF';
    ctx.fillRect(0, 0, newCanvas.width, newCanvas.height);
    
    ctx.drawImage(canvas, 0, 0);
    
    ctx.fillStyle = '#000000';
    ctx.font = 'bold 18px monospace';
    ctx.textAlign = 'center';
    ctx.fillText(text, newCanvas.width / 2, canvas.height + 20);
    
    return newCanvas.toDataURL('image/png');
  };

  const downloadQR = () => {
    const canvas = document.querySelector('#qr-code-wrapper canvas') as HTMLCanvasElement;
    if (canvas) {
      const pngUrl = generateCombinedQRUrl(canvas, qrCode);
      const downloadLink = document.createElement('a');
      downloadLink.href = pngUrl;
      downloadLink.download = `${qrCode || 'qrcode'}.png`;
      document.body.appendChild(downloadLink);
      downloadLink.click();
      document.body.removeChild(downloadLink);
      toast.success('QR Code downloaded successfully');
    } else {
      toast.error('Could not find QR Code to download');
    }
  };

  const printQR = () => {
    const canvas = document.querySelector('#qr-code-wrapper canvas') as HTMLCanvasElement;
    if (canvas) {
      const pngUrl = generateCombinedQRUrl(canvas, qrCode);
      const printWindow = window.open('', '', 'width=600,height=600');
      if (printWindow) {
        printWindow.document.write(`
          <html>
            <head>
              <title>Print QR Code</title>
              <style>
                body { display: flex; flex-direction: column; align-items: center; justify-content: center; height: 100vh; font-family: sans-serif; margin: 0; }
                img { max-width: 100%; height: auto; }
              </style>
            </head>
            <body>
              <img src="${pngUrl}" />
              <script>
                window.onload = function() { window.print(); setTimeout(() => { window.close(); }, 500); }
              </script>
            </body>
          </html>
        `);
        printWindow.document.close();
      }
    } else {
      toast.error('Could not find QR Code to print');
    }
  };

  const triggerScan = () => {
    fileInputRef.current?.click();
  };

  const handleFetchToolByQR = async (code: string) => {
    try {
      toast.info(`Fetching details for ${code}...`);
      const response = await api.get(`/tools/qr/${code}`);
      const tool = response.data;

      setEditingToolId(tool.id);
      setQrCode(tool.qr_code);
      setToolData({
        description: tool.description,
        make: tool.make,
        capacity: tool.capacity,
        safeWorkingLoad: tool.safe_working_load,
        purchaserName: tool.purchaser_name,
        purchaserContact: tool.purchaser_contact,
        dateOfSupply: tool.date_of_supply ? new Date(tool.date_of_supply) : undefined,
        lastInspectionDate: tool.last_inspection_date ? new Date(tool.last_inspection_date) : undefined,
        inspectionResult: 'usable',
        usabilityPercentage: tool.usability_percentage ? String(tool.usability_percentage) : '',
        validityPeriod: tool.validity_period ? String(tool.validity_period) : '',
        subcontractorName: tool.subcontractor_name,
        previousSite: tool.previous_site,
        currentSite: tool.current_site,
        nextSite: tool.next_site,
        supplierCode: tool.supplier_code || '',
        testCertificate: tool.test_certificate || '',
        expiryDate: tool.expiry_date ? new Date(tool.expiry_date) : undefined,
        jobCode: tool.job_code || '',
        jobDescription: tool.job_description || '',
        toolType: tool.tool_type || 'General',
      });
      setIsToolSaved(true);
      toast.success("Tool details loaded!");
      setActiveTab('new'); // Switch to form view
    } catch (error) {
      console.error(error);
      toast.error("Tool not found in database");
    }
  };

  const handleFileUpload = async (e: React.ChangeEvent<HTMLInputElement>) => {
    if (!e.target.files || e.target.files.length === 0) return;
    const file = e.target.files[0];
    setScanning(true);
    const html5QrCode = new Html5Qrcode("reader-hidden-master");
    try {
      const decodedText = await html5QrCode.scanFile(file, true);
      let code = decodedText;
      if (decodedText.includes('/view-tool/')) {
        const parts = decodedText.split('/view-tool/');
        if (parts.length > 1) {
          code = parts[1];
        }
      }
      handleFetchToolByQR(code);
    } catch (err) {
      console.error("Error scanning file", err);
      toast.error("Could not read QR code from image");
    } finally {
      setScanning(false);
      html5QrCode.clear();
    }
  };


  const handleEditTool = (tool: any) => {
    setEditingToolId(tool.id);
    setQrCode(tool.qr_code);
    setToolData({
      description: tool.description,
      make: tool.make,
      capacity: tool.capacity,
      safeWorkingLoad: tool.safe_working_load,
      purchaserName: tool.purchaser_name,
      purchaserContact: tool.purchaser_contact,
      dateOfSupply: tool.date_of_supply ? new Date(tool.date_of_supply) : undefined,
      lastInspectionDate: tool.last_inspection_date ? new Date(tool.last_inspection_date) : undefined,
      inspectionResult: tool.inspection_result || 'usable',
      usabilityPercentage: tool.usability_percentage ? String(tool.usability_percentage) : '',
      validityPeriod: tool.validity_period ? String(tool.validity_period) : '',
      subcontractorName: tool.subcontractor_name,
      previousSite: tool.previous_site,
      currentSite: tool.current_site,
      nextSite: tool.next_site,
      supplierCode: tool.supplier_code || '',
      testCertificate: tool.test_certificate || '',
      expiryDate: tool.expiry_date ? new Date(tool.expiry_date) : undefined,
      jobCode: tool.job_code || '',
      jobDescription: tool.job_description || '',
    });
    setActiveTab('new'); // Switch to Edit Mode (Form)
    setIsToolSaved(true);
    window.scrollTo({ top: 0, behavior: 'smooth' });
    toast.info("Editing tool: " + tool.qr_code);
  };

  const handleViewHistory = async (tool: any) => {
    setHistoryTool(tool);
    try {
      const res = await api.get(`/movements/${tool.id}`);
      setHistoryData(res.data);
      setIsHistoryOpen(true);
    } catch (error) {
      console.error(error);
      toast.error("Failed to load history");
    }
  };

  const handleNewTool = () => {
    setQrCode('');
    setIsToolSaved(false);
    setErrors({});
    setToolData(prev => ({
      ...prev,
      description: '',
      make: new Date().getFullYear().toString(),
      capacity: '',
      safeWorkingLoad: '',
      // Reset other fields as needed, or keep previous values? better reset.
      purchaserName: '',
      purchaserContact: '',
      dateOfSupply: undefined,
      lastInspectionDate: undefined,
      inspectionResult: 'usable',
      usabilityPercentage: '',
      validityPeriod: '',
      subcontractorName: '',
      previousSite: '',
      currentSite: '',
      nextSite: '',
      supplierCode: '',
      testCertificate: '',
      expiryDate: undefined,
    }));
  };


  const handleBulkUpload = async () => {
    if (!importFile) {
      toast.error("Please select an Excel or PDF file first.");
      return;
    }
    const formData = new FormData();
    formData.append("file", importFile);

    setIsUploading(true);
    try {
      const response = await api.post("/upload/tools", formData, {
        headers: { "Content-Type": "multipart/form-data" },
      });
      toast.success(response.data.message || "Bulk import successful");
      if (response.data.errors && response.data.errors.length > 0) {
        toast.warning(`Some rows failed: ${response.data.errors[0]}...`);
      }
      setIsImportModalOpen(false);
      setImportFile(null);
      fetchTools(); // Refresh inventory
      setActiveTab('saved'); // Switch to inventory to see new items
    } catch (error: any) {
      console.error("Bulk upload error", error);
      toast.error(error.response?.data?.detail || "Bulk import failed. Please check file format.");
    } finally {
      setIsUploading(false);
    }
  };

  return (
    <div className="max-w-7xl mx-auto space-y-6 animate-in fade-in duration-500">
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div>
          <h1 className="text-3xl font-semibold text-[#0F172A]">Tool Master</h1>
          <p className="text-gray-500 mt-1">Manage tool inventory, generate QR codes, and track assets.</p>
        </div>
        <Button onClick={() => setIsImportModalOpen(true)} className="bg-indigo-600 hover:bg-indigo-700">
          <UploadCloud className="mr-2 h-4 w-4" /> Bulk Import
        </Button>
      </div>

      {/* Bulk Import Modal */}
      <Dialog open={isImportModalOpen} onOpenChange={setIsImportModalOpen}>
        <DialogContent>
          <DialogHeader>
            <DialogTitle>Bulk Import Tools</DialogTitle>
          </DialogHeader>
          <div className="space-y-4 py-4">
            <p className="text-sm text-gray-500">
              Upload an Excel (.xlsx, .xls) or PDF file containing your tool details. The file must have a table with columns such as Description, Make, Capacity, SWL, etc.
            </p>
            <div className="border-2 border-dashed border-gray-300 rounded-lg p-6 flex flex-col items-center justify-center bg-gray-50">
              <UploadCloud className="h-10 w-10 text-gray-400 mb-2" />
              <Label htmlFor="bulk-file-upload" className="cursor-pointer text-sm font-medium text-blue-600 hover:text-blue-500">
                Click to browse
                <Input
                  id="bulk-file-upload"
                  type="file"
                  accept=".xlsx,.xls,.pdf"
                  className="hidden"
                  onChange={(e) => setImportFile(e.target.files?.[0] || null)}
                />
              </Label>
              {importFile && (
                <p className="text-xs text-green-600 mt-2 flex items-center">
                  <Badge variant="outline" className="bg-green-100 mr-2 border-green-200">Selected</Badge>
                  {importFile.name}
                </p>
              )}
            </div>
          </div>
          <DialogFooter>
            <Button variant="outline" onClick={() => { setIsImportModalOpen(false); setImportFile(null); }}>
              Cancel
            </Button>
            <Button onClick={handleBulkUpload} disabled={!importFile || isUploading} className="bg-indigo-600 hover:bg-indigo-700">
              {isUploading ? "Importing..." : "Start Import"}
            </Button>
          </DialogFooter>
        </DialogContent>
      </Dialog>

      <Tabs value={activeTab} onValueChange={setActiveTab} className="space-y-6">
        <TabsList className="grid w-full grid-cols-2 lg:w-[400px]">
          <TabsTrigger value="new" onClick={handleNewTool}>New Tool Entry</TabsTrigger>
          <TabsTrigger value="saved">Existing Inventory</TabsTrigger>
        </TabsList>

        <TabsContent value="new" className="space-y-6">
          <div className="flex justify-end">
            <div id="reader-hidden-master" className="hidden"></div>
            <input
              type="file"
              accept="image/*"
              capture="environment"
              ref={fileInputRef}
              onChange={handleFileUpload}
              className="hidden"
            />
            <Button
              variant="outline"
              onClick={triggerScan}
              className="border-dashed border-2 border-blue-300 text-blue-700 hover:bg-blue-50"
              disabled={scanning}
            >
              {scanning ? "Scanning..." : "📷 Scan / Upload Existing QR to Autofill"}
            </Button>
          </div>

          <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
            {/* Main Form */}
            <div className="lg:col-span-2 space-y-6">
              {/* Tool Details */}
              <Card>
                <CardHeader>
                  <CardTitle>Tool Details {editingToolId ? '(Editing)' : '(New)'}</CardTitle>
                </CardHeader>
                <CardContent className="space-y-6">
                  <div className="space-y-2">
                    <Label htmlFor="description">Tool Name <span className="text-red-600">*</span></Label>
                    <Select value={toolData.description} onValueChange={(value) => handleInputChange('description', value)} required>
                      <SelectTrigger className={errors.description ? 'border-red-500' : ''}>
                        <SelectValue placeholder="Select tool Name" />
                      </SelectTrigger>
                      <SelectContent className="max-h-[300px]">
                        {TOOLS_LIST.map((tool) => (
                          <SelectItem key={tool} value={tool}>{tool}</SelectItem>
                        ))}
                      </SelectContent>
                    </Select>
                  </div>

                  <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                    <div className="space-y-2">
                      <Label htmlFor="make">Make (Year) <span className="text-red-600">*</span></Label>
                      <Select
                        value={toolData.make}
                        onValueChange={(value) => handleInputChange('make', value)}
                      >
                        <SelectTrigger id="make" className={errors.make ? 'border-red-500' : ''}>
                          <SelectValue placeholder="Select year" />
                        </SelectTrigger>
                        <SelectContent>
                          {Array.from({ length: 30 }, (_, i) => (new Date().getFullYear() - i).toString()).map((year) => (
                            <SelectItem key={year} value={year}>
                              {year}
                            </SelectItem>
                          ))}
                        </SelectContent>
                      </Select>
                    </div>
                    <div className="space-y-2">
                      <Label htmlFor="capacity">Capacity <span className="text-red-600">*</span></Label>
                      <Select
                        value={toolData.capacity}
                        onValueChange={(value) => handleInputChange('capacity', value)}
                      >
                        <SelectTrigger id="capacity" className={errors.capacity ? 'border-red-500' : ''}>
                          <SelectValue placeholder="Select Capacity" />
                        </SelectTrigger>
                        <SelectContent className="max-h-[200px]">
                          {Array.from({ length: 50 }, (_, i) => i + 1).map((num) => (
                            <SelectItem key={num} value={`${num} ${num === 1 ? 'Tonne' : 'Tonnes'}`}>
                              {num} {num === 1 ? 'Tonne' : 'Tonnes'}
                            </SelectItem>
                          ))}
                        </SelectContent>
                      </Select>
                    </div>
                    <div className="space-y-2">
                      <Label htmlFor="swl">Safe Working Load (SWL) <span className="text-red-600">*</span></Label>
                      <Select
                        value={toolData.safeWorkingLoad}
                        onValueChange={(value) => handleInputChange('safeWorkingLoad', value)}
                      >
                        <SelectTrigger id="swl" className={errors.safeWorkingLoad ? 'border-red-500' : ''}>
                          <SelectValue placeholder="Select SWL" />
                        </SelectTrigger>
                        <SelectContent className="max-h-[200px]">
                          {Array.from({ length: 50 }, (_, i) => i + 1).map((num) => (
                            <SelectItem key={num} value={`${num} ${num === 1 ? 'Tonne' : 'Tonnes'}`}>
                              {num} {num === 1 ? 'Tonne' : 'Tonnes'}
                            </SelectItem>
                          ))}
                        </SelectContent>
                      </Select>
                    </div>
                  </div>
                </CardContent>
              </Card>

              {/* Supplier Details */}
              <Card>
                <CardHeader>
                  <CardTitle>Supplier Details</CardTitle>
                </CardHeader>
                <CardContent className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <div className="space-y-2">
                    <Label htmlFor="purchaser">Supplier Name <span className="text-red-600">*</span></Label>
                    <Input
                      id="purchaser"
                      placeholder="Enter supplier name"
                      value={toolData.purchaserName}
                      onChange={(e) => handleInputChange('purchaserName', e.target.value)}
                      className={errors.purchaserName ? 'border-red-500' : ''}
                    />
                  </div>
                  <div className="space-y-2">
                    <Label htmlFor="contact">Supplier Contact Number <span className="text-red-600">*</span></Label>
                    <Input
                      id="contact"
                      placeholder="Enter contact number"
                      value={toolData.purchaserContact}
                      onChange={(e) => handleInputChange('purchaserContact', e.target.value)}
                      className={errors.purchaserContact ? 'border-red-500' : ''}
                    />
                  </div>
                  <div className="space-y-2">
                    <Label htmlFor="supplierCode">Supplier Code ({toolData.supplierCode ? toolData.supplierCode.padEnd(3, '0').substring(0, 3).toUpperCase() : 'XXX'}) <span className="text-red-600">*</span></Label>
                    <Input
                      id="supplierCode"
                      placeholder="e.g. 001"
                      maxLength={3}
                      value={toolData.supplierCode}
                      onChange={(e) => handleInputChange('supplierCode', e.target.value)}
                      className={errors.supplierCode ? 'border-red-500' : ''}
                    />
                  </div>
                  <div className="space-y-2">
                    <Label htmlFor="testCert">Test Certificate (PDF/Image)</Label>
                    <div className="flex gap-2 items-center">
                      <Input
                        id="testCert"
                        type="file"
                        accept=".pdf,.jpg,.jpeg,.png"
                        onChange={handleCertUpload}
                        className="cursor-pointer"
                      />
                      {toolData.testCertificate && (
                        <a
                          href={`http://localhost:8000${toolData.testCertificate}`}
                          target="_blank"
                          rel="noreferrer"
                          className="text-blue-600 hover:underline text-sm"
                        >
                          View Uploaded
                        </a>
                      )}
                    </div>
                  </div>
                  <div className="space-y-2 md:col-span-2">
                    <Label htmlFor="dateOfSupply">Date of Receipt <span className="text-red-600">*</span></Label>
                    <div className={errors.dateOfSupply ? 'border rounded-md border-red-500' : ''}>
                      <DatePicker
                        date={toolData.dateOfSupply}
                        onDateChange={(date) => handleDateChange('dateOfSupply', date)}
                      />
                    </div>
                  </div>
                  {/* Validity Info */}
                  {toolData.dateOfSupply && (
                    <>
                      <div className="space-y-2">
                        <Label htmlFor="validityPeriod">Validity Period (Years)</Label>
                        <div className="h-10 px-3 py-2 rounded-md border border-input bg-gray-100 text-sm opacity-80 cursor-not-allowed">
                          {toolData.validityPeriod || 'Automatically calculated'}
                        </div>
                      </div>

                      <div className="space-y-2">
                        <Label htmlFor="expiryDate">Expiry Date</Label>
                        <div className="h-10 px-3 py-2 rounded-md border border-input bg-gray-100 text-sm opacity-80 cursor-not-allowed">
                          {toolData.expiryDate ? toolData.expiryDate.toLocaleDateString() : 'Auto-calculated'}
                        </div>
                      </div>
                    </>
                  )}
                </CardContent>
              </Card>

              <Card>
                <CardHeader>
                  <CardTitle>Job Details</CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                    <div className="space-y-2">
                      <Label htmlFor="jobCode">Job Code <span className="text-red-600">*</span></Label>
                      <Input
                        id="jobCode"
                        placeholder="Enter Job Code"
                        value={toolData.jobCode}
                        onChange={e => handleInputChange('jobCode', e.target.value)}
                        className={errors.jobCode ? 'border-red-500' : ''}
                      />
                    </div>
                    <div className="space-y-2">
                      <Label htmlFor="jobDescription">Job Description <span className="text-red-600">*</span></Label>
                      <Input
                        id="jobDescription"
                        placeholder="Enter Job Description"
                        value={toolData.jobDescription}
                        onChange={e => handleInputChange('jobDescription', e.target.value)}
                        className={errors.jobDescription ? 'border-red-500' : ''}
                      />
                    </div>
                  </div>
                </CardContent>
              </Card>

              {/* Inspection Status - Only for Existing Tools (Editing) */}
              {editingToolId && (
                <Card>
                  <CardHeader>
                    <CardTitle>Inspection Status</CardTitle>
                  </CardHeader>
                  <CardContent className="space-y-4">
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                      <div className="space-y-2">
                        <Label htmlFor="lastInspection">Date of Last Inspection</Label>
                        <DatePicker
                          date={toolData.lastInspectionDate}
                          onDateChange={(date) => handleDateChange('lastInspectionDate', date)}
                        />
                      </div>
                    </div>
                    <div className="space-y-3">
                      <Label>Inspection Result</Label>
                      <RadioGroup
                        value={toolData.inspectionResult}
                        onValueChange={(value) => handleInputChange('inspectionResult', value)}
                      >
                        <div className="flex items-center space-x-2">
                          <RadioGroupItem value="usable" id="usable" />
                          <Label htmlFor="usable" className="font-normal cursor-pointer">Usable</Label>
                        </div>
                        <div className="flex items-center space-x-2">
                          <RadioGroupItem value="not-usable" id="not-usable" />
                          <Label htmlFor="not-usable" className="font-normal cursor-pointer">Not Usable</Label>
                        </div>
                      </RadioGroup>
                    </div>
                    {toolData.inspectionResult === 'usable' && (
                      <div className="grid grid-cols-1 md:grid-cols-2 gap-4 pt-4 border-t">
                        <div className="space-y-2">
                          <Label htmlFor="usability">Usability Percentage</Label>
                          <Input
                            id="usability"
                            type="number"
                            placeholder="e.g., 95"
                            value={toolData.usabilityPercentage}
                            onChange={(e) => handleInputChange('usabilityPercentage', e.target.value)}
                          />
                        </div>
                      </div>
                    )}
                  </CardContent>
                </Card>
              )}



              <Button className="w-full bg-[#1E3A8A] h-12 text-lg" onClick={handleSave}>
                <Save className="mr-2 h-5 w-5" />
                {editingToolId ? 'Update Tool Details' : 'Save Tool Details'}
              </Button>
            </div>

            {/* QR Code Panel */}
            <div className="lg:col-span-1">
              <Card className="sticky top-24">
                <CardHeader>
                  <CardTitle>QR Code</CardTitle>
                </CardHeader>
                <CardContent className="space-y-4">
                  {isToolSaved && qrCode ? (
                    <div className="flex flex-col items-center space-y-4">
                      <div className="p-4 bg-white border-2 border-gray-200 rounded-lg" id="qr-code-wrapper">
                        <QRCodeCanvas
                          value={`${baseUrl}/view-tool/${qrCode}`}
                          size={200}
                          level={"H"}
                          includeMargin={true}
                        />
                      </div>
                      <div className="text-center">
                        <p className="text-sm text-gray-500">Scan to View Details</p>
                        <p className="font-mono font-medium text-xs text-gray-400">{qrCode}</p>
                      </div>
                      <div className="grid grid-cols-2 gap-2 w-full">
                        <Button variant="outline" size="sm" onClick={downloadQR}>
                          <Download className="w-4 h-4 mr-2" />
                          Download
                        </Button>
                        <Button variant="outline" size="sm" onClick={printQR}>
                          <Printer className="w-4 h-4 mr-2" />
                          Print
                        </Button>
                      </div>
                      <p className="text-xs text-center text-amber-600 bg-amber-50 p-2 rounded">
                        Note: Ensure your mobile is on the same network and you are accessing this site via IP address for mobile scanning to work.
                      </p>
                    </div>
                  ) : (
                    <div className="text-center py-12">
                      <p className="text-gray-400 mb-4">QR Code will be generated automatically after saving the tool details.</p>
                      <Button disabled variant="outline">Auto-Generated on Save</Button>
                    </div>
                  )}
                </CardContent>
              </Card>
            </div>
          </div >
        </TabsContent >

        <TabsContent value="saved" className="space-y-6">
          <div className="flex flex-col md:flex-row gap-4 mb-6">
            <div className="relative flex-1">
              <Search className="absolute left-2.5 top-2.5 h-4 w-4 text-gray-500" />
              <Input
                placeholder="Search by Name, QR, Make or Site..."
                className="pl-9"
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
              />
            </div>
            <div className="w-full md:w-[200px]">
              <Select value={statusFilter} onValueChange={setStatusFilter}>
                <SelectTrigger>
                  <SelectValue placeholder="Filter by Status" />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="all">All Status</SelectItem>
                  <SelectItem value="usable">Usable</SelectItem>
                  <SelectItem value="scrap">Scrap</SelectItem>
                </SelectContent>
              </Select>
            </div>
          </div>

          <div className="rounded-md border bg-white shadow-sm overflow-hidden">
            <Table>
              <TableHeader className="bg-gray-50">
                <TableRow>
                  <TableHead>Tool Name</TableHead>
                  <TableHead>QR Code</TableHead>
                  <TableHead>Make</TableHead>
                  <TableHead>Capacity</TableHead>
                  <TableHead>Current Site</TableHead>
                  <TableHead>Status</TableHead>
                  <TableHead className="text-center">QR</TableHead>
                  <TableHead className="text-right">Actions</TableHead>
                </TableRow>
              </TableHeader>
              <TableBody>
                {filteredTools.length > 0 ? (
                  filteredTools.map((tool) => (
                    <TableRow key={tool.id} className="hover:bg-gray-50/50">
                      <TableCell className="font-medium text-[#1E3A8A]">
                        <span
                          className="cursor-pointer underline decoration-dotted underline-offset-4 decoration-gray-400 hover:text-blue-700 hover:decoration-blue-700 transition-colors"
                          onMouseEnter={() => setHoveredTool(tool)}
                        >
                          {tool.description}
                        </span>
                      </TableCell>
                      <TableCell className="font-mono text-xs">{tool.qr_code}</TableCell>
                      <TableCell>{tool.make}</TableCell>
                      <TableCell>{tool.capacity}</TableCell>
                      <TableCell>{tool.current_site || '-'}</TableCell>
                      <TableCell>
                        <span className={`px-2 py-1 rounded text-xs font-semibold capitalize ${tool.status === 'usable' ? 'bg-green-100 text-green-700' : 'bg-red-100 text-red-700'
                          }`}>
                          {tool.status}
                        </span>
                      </TableCell>
                      <TableCell className="text-center">
                        <div className="hidden" id={`qr-wrapper-list-${tool.id}`}>
                          <QRCodeCanvas
                            value={`${baseUrl}/view-tool/${tool.qr_code}`}
                            size={200}
                            level={"H"}
                            includeMargin={true}
                          />
                        </div>
                        <Button
                          variant="ghost"
                          size="icon"
                          title="Download QR"
                          className="h-8 w-8 text-blue-600 hover:bg-blue-50"
                          onClick={() => {
                            const wrapper = document.getElementById(`qr-wrapper-list-${tool.id}`);
                            const canvas = wrapper?.querySelector('canvas');
                            if (canvas) {
                              const pngUrl = generateCombinedQRUrl(canvas, tool.qr_code);
                              const downloadLink = document.createElement('a');
                              downloadLink.href = pngUrl;
                              downloadLink.download = `QR-${tool.qr_code}.png`;
                              document.body.appendChild(downloadLink);
                              downloadLink.click();
                              document.body.removeChild(downloadLink);
                              toast.success(`Downloaded QR: ${tool.qr_code}`);
                            } else {
                              toast.error('Could not generate QR');
                            }
                          }}
                        >
                          <Download className="h-4 w-4" />
                        </Button>
                      </TableCell>
                      <TableCell className="text-right">
                        <div className="flex justify-end gap-2">
                          <Button
                            variant="ghost"
                            size="sm"
                            className="h-8 w-8 p-0"
                            onClick={() => handleEditTool(tool)}
                          >
                            <Edit className="h-4 w-4 text-gray-500 hover:text-blue-700" />
                          </Button>
                          <Button
                            variant="ghost"
                            size="sm"
                            className="h-8 w-8 p-0"
                            title="View Movement History"
                            onClick={() => handleViewHistory(tool)}
                          >
                            <History className="h-4 w-4 text-gray-500 hover:text-blue-700" />
                          </Button>
                        </div>
                      </TableCell>
                    </TableRow>
                  ))
                ) : (
                  <TableRow>
                    <TableCell colSpan={8} className="h-24 text-center">
                      No tools found matching your criteria.
                    </TableCell>
                  </TableRow>
                )}
              </TableBody>
            </Table>
          </div>
        </TabsContent>
      </Tabs>

      {/* History Dialog */}
      <Dialog open={isHistoryOpen} onOpenChange={setIsHistoryOpen}>
        <DialogContent className="max-w-3xl max-h-[80vh] overflow-y-auto">
          <DialogHeader>
            <DialogTitle className="flex items-center gap-2">
              <History className="w-5 h-5 text-gray-500" />
              Movement History: {historyTool?.description}
              <Badge variant="outline">{historyTool?.qr_code}</Badge>
            </DialogTitle>
          </DialogHeader>

          <div className="mt-4">
            <Table>
              <TableHeader>
                <TableRow>
                  <TableHead>Time</TableHead>
                  <TableHead>From</TableHead>
                  <TableHead>To</TableHead>
                  <TableHead>Remarks</TableHead>
                </TableRow>
              </TableHeader>
              <TableBody>
                {historyData.length > 0 ? (
                  historyData.map((record) => (
                    <TableRow key={record.id}>
                      <TableCell className="text-xs text-gray-500">
                        {new Date(record.timestamp).toLocaleString()}
                      </TableCell>
                      <TableCell className="text-gray-700">{record.from_site || '-'}</TableCell>
                      <TableCell className="font-semibold text-blue-700">{record.to_site || '-'}</TableCell>
                      <TableCell className="text-sm text-gray-600">{record.remarks || '-'}</TableCell>
                    </TableRow>
                  ))
                ) : (
                  <TableRow>
                    <TableCell colSpan={4} className="text-center py-8 text-gray-500">
                      No movement history recorded yet.
                    </TableCell>
                  </TableRow>
                )}
              </TableBody>
            </Table>
          </div>
        </DialogContent>
      </Dialog>
      {/* Spotlight Overlay & Centered Card */}
      {hoveredTool && (
        <div className="fixed inset-0 z-50 flex items-center justify-center isolate" onClick={() => setHoveredTool(null)}>
          {/* Backdrop Blur */}
          <div className="absolute inset-0 bg-black/40 backdrop-blur-md" aria-hidden="true" />

          {/* Centered Card */}
          <div className="relative z-50 w-96 p-6 bg-white/95 shadow-2xl rounded-xl border border-white/20 animate-in zoom-in-95 duration-200">
            <div className="space-y-4">
              <div className="flex justify-between items-start gap-4">
                <div>
                  <h4 className="text-lg font-bold text-[#1E3A8A] flex items-center gap-2">
                    {hoveredTool.description}
                    <Badge variant="outline" className="text-xs bg-blue-50 text-blue-700 border-blue-200">{hoveredTool.qr_code}</Badge>
                  </h4>
                  <p className="text-sm text-gray-500 mt-1">{hoveredTool.make} • {hoveredTool.capacity} • SWL {hoveredTool.safe_working_load}</p>
                </div>
                <div className="p-2 bg-white rounded-lg border shadow-sm shrink-0">
                  <QRCodeCanvas
                    value={`${baseUrl}/view-tool/${hoveredTool.qr_code}`}
                    size={64}
                    level={"H"}
                    includeMargin={true}
                  />
                </div>
              </div>

              <div className="grid grid-cols-2 gap-4 text-sm border-t border-b py-4">
                <div>
                  <span className="text-gray-500 block text-xs">Supplier</span>
                  <span className="font-medium">{hoveredTool.purchaser_name || '-'}</span>
                  {hoveredTool.supplier_code && <span className="block text-gray-400 text-[10px]">Code: {hoveredTool.supplier_code}</span>}
                  {hoveredTool.purchaser_contact && <span className="block text-gray-400 text-[10px]">Contact: {hoveredTool.purchaser_contact}</span>}
                </div>
                <div>
                  <span className="text-gray-500 block text-xs">Date of Receipt</span>
                  <span className="font-medium">{hoveredTool.date_of_supply ? new Date(hoveredTool.date_of_supply).toLocaleDateString() : '-'}</span>
                  {hoveredTool.validity_period && <span className="block text-gray-400 text-[10px]">Validity: {hoveredTool.validity_period} Years</span>}
                </div>
                <div>
                  <span className="text-gray-500 block text-xs">Last Inspection</span>
                  <span className="font-medium">{hoveredTool.last_inspection_date ? new Date(hoveredTool.last_inspection_date).toLocaleDateString() : '-'}</span>
                  <div className="flex items-center gap-2">
                    <span className={`text-xs font-semibold capitalize ${hoveredTool.inspection_result === 'usable' ? 'text-green-600' : 'text-red-500'}`}>
                      {hoveredTool.inspection_result}
                    </span>
                    {hoveredTool.usability_percentage && <span className="text-[10px] text-gray-500">({hoveredTool.usability_percentage}%)</span>}
                  </div>
                </div>
                <div>
                  <span className="text-gray-500 block text-xs">Valid Until</span>
                  <span className="font-medium">{hoveredTool.expiry_date ? new Date(hoveredTool.expiry_date).toLocaleDateString() : '-'}</span>
                </div>
              </div>

              <div className="grid grid-cols-2 gap-4 text-sm border-b py-4">
                <div>
                  <span className="text-gray-500 block text-xs">Job Code</span>
                  <span className="font-medium">{hoveredTool.job_code || '-'}</span>
                </div>
                <div>
                  <span className="text-gray-500 block text-xs">Job Description</span>
                  <span className="font-medium truncate" title={hoveredTool.job_description}>{hoveredTool.job_description || '-'}</span>
                </div>
              </div>

              {hoveredTool.debit_to && (
                <div className="py-2 border-b bg-red-50 px-3 rounded mb-2">
                  <span className="text-red-600 font-semibold block text-xs">Liability / Debit</span>
                  <span className="text-sm font-bold text-red-800">{hoveredTool.debit_to}</span>
                </div>
              )}

              <div className="text-sm space-y-2">
                <p className="font-semibold text-gray-700">Site Movement History</p>
                <div className="grid grid-cols-2 gap-2 text-xs text-center">
                  <div className="bg-gray-100 p-2 rounded">
                    <span className="block text-gray-500 text-[10px] uppercase">Previous</span>
                    {hoveredTool.previous_site || '-'}
                  </div>
                  <div className="bg-blue-50 text-blue-800 p-2 rounded ring-1 ring-blue-100">
                    <span className="block text-blue-400 text-[10px] uppercase">Current</span>
                    <span className="font-bold">{hoveredTool.current_site || '-'}</span>
                  </div>
                </div>
                {hoveredTool.subcontractor_name && (
                  <div className="mt-1 pt-1 border-t border-dashed text-xs">
                    <span className="text-gray-500">Sub-contractor: </span>
                    <span className="font-medium">{hoveredTool.subcontractor_name}</span>
                    {hoveredTool.subcontractor_code && <span className="text-gray-400"> ({hoveredTool.subcontractor_code})</span>}
                  </div>
                )}
              </div>

              {(hoveredTool.remarks || hoveredTool.test_certificate) && (
                <div className="pt-2 text-xs space-y-2 border-t mt-2">
                  {hoveredTool.remarks && (
                    <div>
                      <span className="text-gray-500 font-semibold">Remarks: </span>
                      <span className="text-gray-700">{hoveredTool.remarks}</span>
                    </div>
                  )}
                  {hoveredTool.test_certificate && (
                    <div className="flex items-center gap-2 mt-1">
                      <span className="text-gray-500 font-semibold">Certificate: </span>
                      <a
                        href={`http://localhost:8000${hoveredTool.test_certificate}`}
                        target="_blank"
                        rel="noreferrer"
                        className="flex items-center text-blue-600 hover:text-blue-800 font-medium bg-blue-50 px-2 py-1 rounded border border-blue-100 transition-colors"
                        onClick={(e) => e.stopPropagation()}
                      >
                        <Download className="w-3 h-3 mr-1" />
                        Download PDF
                      </a>
                    </div>
                  )}
                </div>
              )}
            </div>
          </div>
        </div>
      )}
    </div >
  );
};

export default ToolMaster;