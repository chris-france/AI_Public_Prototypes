export default function HardwareTable({ gpus, selected }) {
  return (
    <div className="bg-white rounded-xl shadow-sm border border-gray-200 overflow-hidden">
      <div className="px-6 py-4 border-b border-gray-100">
        <h3 className="font-semibold text-gray-900">Hardware Reference</h3>
        <p className="text-xs text-gray-500 mt-0.5">Selected: {selected}</p>
      </div>
      <div className="overflow-x-auto">
        <table className="w-full text-sm">
          <thead>
            <tr className="bg-gray-50 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
              <th className="px-6 py-3">GPU Model</th>
              <th className="px-6 py-3 text-right">Purchase Price</th>
              <th className="px-6 py-3 text-right">TDP (Watts)</th>
              <th className="px-6 py-3 text-right">VRAM (GB)</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-gray-100">
            {Object.entries(gpus).map(([name, specs]) => (
              <tr key={name} className={name === selected ? 'bg-france-blue/10 font-semibold text-france-blue' : ''}>
                <td className="px-6 py-3">{name}</td>
                <td className="px-6 py-3 text-right">${specs.cost.toLocaleString()}</td>
                <td className="px-6 py-3 text-right">{specs.watts}</td>
                <td className="px-6 py-3 text-right">{specs.vram}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  )
}
