import React, { useState } from 'react';
import { GraduationCap, BookOpen, Users, TrendingUp, Award, Brain, ChevronRight, CheckCircle, Clock, AlertTriangle, BarChart3 } from 'lucide-react';

// Mock data - matches your Jupyter prototype
const mockData = {
  users: {
    teacher1: { id: 'teacher1', name: 'Ms. Johnson', role: 'teacher' },
    student1: { id: 'student1', name: 'Emma Wilson', role: 'student', grade: 7 }
  },
  courses: {
    math7: { id: 'math7', name: 'Grade 7 Mathematics', teacher: 'Ms. Johnson', students: 3, assignments: 2 },
    science7: { id: 'science7', name: 'Grade 7 Science', teacher: 'Ms. Johnson', students: 3, assignments: 1 }
  },
  assignments: {
    a1: { 
      id: 'a1', 
      title: 'Fractions Quiz', 
      description: 'Complete problems 1-20 on fractions',
      dueDate: '2025-12-14',
      points: 100,
      difficulty: 'medium',
      status: 'pending'
    },
    a2: {
      id: 'a2',
      title: 'Geometry Project',
      description: 'Create a presentation on geometric shapes',
      dueDate: '2025-12-18',
      points: 150,
      difficulty: 'hard',
      status: 'not_submitted'
    }
  },
  submissions: {
    s1: {
      id: 's1',
      student: 'Emma Wilson',
      assignment: 'Fractions Quiz',
      content: 'Completed all 20 problems with detailed work shown. Applied cross-multiplication method for complex fractions and showed step-by-step solutions.',
      submitted: '2025-12-10',
      grade: null,
      aiScore: null,
      feedback: null
    }
  },
  studentPerformance: {
    student1: {
      scores: [88, 92, 95, 90, 87],
      strength: 'math',
      weakness: 'writing',
      trend: 'improving'
    }
  }
};

const LMSDemo = () => {
  const [currentView, setCurrentView] = useState('login');
  const [currentUser, setCurrentUser] = useState(null);
  const [activeTab, setActiveTab] = useState('courses');
  const [submissions, setSubmissions] = useState(mockData.submissions);
  const [showAIGrading, setShowAIGrading] = useState(false);

  // AI Grading Function
  const gradeWithAI = (submissionId) => {
    setShowAIGrading(true);
    
    setTimeout(() => {
      const submission = submissions[submissionId];
      const contentLength = submission.content.length;
      const qualityScore = Math.min(100, contentLength / 3);
      const difficulty = mockData.assignments[submission.assignment.replace(' ', '').toLowerCase().replace('quiz', '').replace('fractions', 'a1')];
      
      let score = Math.round(qualityScore * 0.98);
      let feedback = '';
      let suggestions = [];

      if (score >= 90) {
        feedback = "Outstanding work! Demonstrates deep understanding. ";
        suggestions = ["Consider exploring advanced applications of these concepts."];
      } else if (score >= 80) {
        feedback = "Good work! Shows solid grasp of the material. ";
        suggestions = ["Review key concepts again to strengthen understanding.", "Add more examples to support your points."];
      }

      setSubmissions(prev => ({
        ...prev,
        [submissionId]: {
          ...prev[submissionId],
          grade: score,
          aiScore: score,
          feedback: feedback + "Suggestions: " + suggestions.join("; ")
        }
      }));
      
      setTimeout(() => setShowAIGrading(false), 2000);
    }, 1500);
  };

  // Login Screen
  const LoginScreen = () => (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 flex items-center justify-center p-4">
      <div className="max-w-4xl w-full">
        <div className="bg-gradient-to-r from-indigo-600 to-purple-600 rounded-2xl shadow-2xl p-8 text-white text-center mb-8">
          <div className="flex items-center justify-center mb-4">
            <GraduationCap className="w-16 h-16" />
          </div>
          <h1 className="text-4xl font-bold mb-2">K-12 Learning Management System</h1>
          <p className="text-xl text-indigo-100">AI-Powered Educational Platform</p>
          <p className="mt-4 text-indigo-200">Empowering teachers and students with intelligent learning tools</p>
        </div>

        <div className="bg-white rounded-xl shadow-xl p-8">
          <h2 className="text-2xl font-bold text-gray-800 text-center mb-6">Select a user to login</h2>
          
          <div className="mb-6">
            <div className="flex items-center mb-4">
              <Users className="w-5 h-5 text-blue-600 mr-2" />
              <h3 className="text-lg font-semibold text-gray-700">Teacher Accounts</h3>
            </div>
            <button
              onClick={() => { setCurrentUser(mockData.users.teacher1); setCurrentView('teacher'); }}
              className="w-full bg-blue-500 hover:bg-blue-600 text-white py-3 px-4 rounded-lg font-medium transition-colors flex items-center justify-between"
            >
              <span>👨‍🏫 Ms. Johnson</span>
              <ChevronRight className="w-5 h-5" />
            </button>
          </div>

          <div>
            <div className="flex items-center mb-4">
              <GraduationCap className="w-5 h-5 text-green-600 mr-2" />
              <h3 className="text-lg font-semibold text-gray-700">Student Accounts</h3>
            </div>
            <button
              onClick={() => { setCurrentUser(mockData.users.student1); setCurrentView('student'); }}
              className="w-full bg-green-500 hover:bg-green-600 text-white py-3 px-4 rounded-lg font-medium transition-colors flex items-center justify-between"
            >
              <span>👨‍🎓 Emma Wilson (Grade 7)</span>
              <ChevronRight className="w-5 h-5" />
            </button>
          </div>
        </div>

        <div className="mt-8 bg-purple-50 rounded-xl p-6 border-2 border-purple-200">
          <h3 className="text-xl font-bold text-purple-900 text-center mb-4 flex items-center justify-center">
            <Brain className="w-6 h-6 mr-2" />
            AI-Powered Features
          </h3>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div className="bg-white p-4 rounded-lg">
              <div className="font-semibold text-gray-800">✨ Automated Grading</div>
              <div className="text-sm text-gray-600 mt-1">AI assists teachers with intelligent grading and feedback</div>
            </div>
            <div className="bg-white p-4 rounded-lg">
              <div className="font-semibold text-gray-800">🎯 Personalized Paths</div>
              <div className="text-sm text-gray-600 mt-1">Custom learning recommendations based on performance</div>
            </div>
            <div className="bg-white p-4 rounded-lg">
              <div className="font-semibold text-gray-800">📊 Smart Analytics</div>
              <div className="text-sm text-gray-600 mt-1">Performance prediction and progress tracking</div>
            </div>
            <div className="bg-white p-4 rounded-lg">
              <div className="font-semibold text-gray-800">📚 Content Recommendations</div>
              <div className="text-sm text-gray-600 mt-1">Study materials matched to student level</div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );

  // Teacher Dashboard
  const TeacherDashboard = () => (
    <div className="min-h-screen bg-gray-50">
      <div className="bg-gradient-to-r from-indigo-600 to-purple-600 text-white p-6 shadow-lg">
        <div className="max-w-7xl mx-auto">
          <h1 className="text-3xl font-bold mb-2">👨‍🏫 Teacher Dashboard - Welcome, {currentUser.name}!</h1>
          <p className="text-indigo-100">Manage your courses, grade assignments, and track student progress</p>
        </div>
      </div>

      <div className="max-w-7xl mx-auto p-6">
        <div className="bg-white rounded-xl shadow-md mb-6">
          <div className="flex border-b">
            <button
              onClick={() => setActiveTab('courses')}
              className={`flex-1 py-4 px-6 font-medium ${activeTab === 'courses' ? 'border-b-2 border-indigo-600 text-indigo-600' : 'text-gray-600'}`}
            >
              📚 My Courses
            </button>
            <button
              onClick={() => setActiveTab('grade')}
              className={`flex-1 py-4 px-6 font-medium ${activeTab === 'grade' ? 'border-b-2 border-indigo-600 text-indigo-600' : 'text-gray-600'}`}
            >
              📝 Grade Assignments
            </button>
            <button
              onClick={() => setActiveTab('analytics')}
              className={`flex-1 py-4 px-6 font-medium ${activeTab === 'analytics' ? 'border-b-2 border-indigo-600 text-indigo-600' : 'text-gray-600'}`}
            >
              📊 Analytics
            </button>
          </div>

          <div className="p-6">
            {activeTab === 'courses' && (
              <div className="space-y-4">
                {Object.values(mockData.courses).map(course => (
                  <div key={course.id} className="border-2 border-indigo-200 rounded-lg p-6 bg-indigo-50">
                    <h3 className="text-xl font-bold text-indigo-900 mb-2">{course.name}</h3>
                    <p className="text-gray-700 mb-3">
                      <span className="font-semibold">Teacher:</span> {course.teacher}
                    </p>
                    <div className="flex gap-4 text-sm text-gray-600">
                      <span>👥 {course.students} students</span>
                      <span>📝 {course.assignments} assignments</span>
                    </div>
                  </div>
                ))}
              </div>
            )}

            {activeTab === 'grade' && (
              <div className="space-y-6">
                {showAIGrading && (
                  <div className="bg-blue-50 border-2 border-blue-500 rounded-lg p-6 animate-pulse">
                    <div className="flex items-center">
                      <Brain className="w-8 h-8 text-blue-600 mr-3 animate-spin" />
                      <div>
                        <h4 className="text-lg font-bold text-blue-900">AI is analyzing submission...</h4>
                        <p className="text-blue-700">Evaluating content quality, completeness, and understanding</p>
                      </div>
                    </div>
                  </div>
                )}

                {Object.entries(submissions).map(([id, sub]) => (
                  <div key={id} className={`border-2 rounded-lg p-6 ${sub.grade !== null ? 'border-green-300 bg-green-50' : 'border-orange-300 bg-orange-50'}`}>
                    <h3 className="text-xl font-bold text-gray-900 mb-2">{sub.assignment}</h3>
                    <p className="text-gray-700 mb-2">
                      <span className="font-semibold">Student:</span> {sub.student} | 
                      <span className="font-semibold ml-2">Submitted:</span> {sub.submitted}
                    </p>
                    <div className="bg-white p-4 rounded-lg mb-4">
                      <p className="text-gray-800"><span className="font-semibold">Content:</span> {sub.content}</p>
                    </div>

                    {sub.grade === null ? (
                      <button
                        onClick={() => gradeWithAI(id)}
                        disabled={showAIGrading}
                        className="bg-indigo-600 hover:bg-indigo-700 disabled:bg-gray-400 text-white py-2 px-6 rounded-lg font-medium flex items-center transition-colors"
                      >
                        <Brain className="w-5 h-5 mr-2" />
                        🤖 AI Grade This Assignment
                      </button>
                    ) : (
                      <div className="bg-white border-2 border-green-500 rounded-lg p-4">
                        <div className="flex items-center mb-2">
                          <CheckCircle className="w-6 h-6 text-green-600 mr-2" />
                          <h4 className="text-lg font-bold text-green-900">Graded with AI Assistance!</h4>
                        </div>
                        <p className="text-gray-800 mb-2">
                          <span className="font-semibold">Score:</span> <span className="text-2xl text-green-600">{sub.grade}%</span>
                        </p>
                        <p className="text-gray-700">
                          <span className="font-semibold">AI Feedback:</span> {sub.feedback}
                        </p>
                      </div>
                    )}
                  </div>
                ))}
              </div>
            )}

            {activeTab === 'analytics' && (
              <div className="space-y-6">
                <div className="bg-indigo-50 border-2 border-indigo-300 rounded-lg p-6">
                  <h3 className="text-xl font-bold text-indigo-900 mb-4 flex items-center">
                    <BarChart3 className="w-6 h-6 mr-2" />
                    Overall Class Performance
                  </h3>
                  <div className="grid grid-cols-3 gap-4">
                    <div className="bg-white p-4 rounded-lg text-center">
                      <div className="text-3xl font-bold text-indigo-600">88.5%</div>
                      <div className="text-sm text-gray-600 mt-1">Average Score</div>
                    </div>
                    <div className="bg-white p-4 rounded-lg text-center">
                      <div className="text-3xl font-bold text-green-600">95%</div>
                      <div className="text-sm text-gray-600 mt-1">Highest Score</div>
                    </div>
                    <div className="bg-white p-4 rounded-lg text-center">
                      <div className="text-3xl font-bold text-orange-600">82%</div>
                      <div className="text-sm text-gray-600 mt-1">Lowest Score</div>
                    </div>
                  </div>
                </div>

                <div className="bg-white border-2 border-gray-200 rounded-lg p-6">
                  <h4 className="text-lg font-bold text-gray-900 mb-4">Grade Distribution</h4>
                  <div className="space-y-3">
                    {[
                      { range: '90-100%', count: 2, color: 'bg-green-500', width: '40%' },
                      { range: '80-89%', count: 3, color: 'bg-blue-500', width: '60%' },
                      { range: '70-79%', count: 1, color: 'bg-yellow-500', width: '20%' },
                      { range: '60-69%', count: 0, color: 'bg-orange-500', width: '0%' },
                      { range: '0-59%', count: 0, color: 'bg-red-500', width: '0%' }
                    ].map(item => (
                      <div key={item.range} className="flex items-center gap-3">
                        <div className="w-24 text-sm font-medium text-gray-700">{item.range}</div>
                        <div className="flex-1 bg-gray-200 rounded-full h-8">
                          <div className={`${item.color} h-8 rounded-full flex items-center justify-center text-white font-medium`} style={{ width: item.width }}>
                            {item.count > 0 && `${item.count} student${item.count > 1 ? 's' : ''}`}
                          </div>
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
              </div>
            )}
          </div>
        </div>

        <button
          onClick={() => { setCurrentUser(null); setCurrentView('login'); }}
          className="bg-red-500 hover:bg-red-600 text-white py-2 px-6 rounded-lg font-medium transition-colors"
        >
          Logout
        </button>
      </div>
    </div>
  );

  // Student Dashboard
  const StudentDashboard = () => {
    const performance = mockData.studentPerformance.student1;
    const avgScore = performance.scores.reduce((a, b) => a + b, 0) / performance.scores.length;
    
    return (
      <div className="min-h-screen bg-gray-50">
        <div className="bg-gradient-to-r from-cyan-500 to-blue-600 text-white p-6 shadow-lg">
          <div className="max-w-7xl mx-auto">
            <h1 className="text-3xl font-bold mb-2">👨‍🎓 Student Dashboard - Welcome, {currentUser.name}!</h1>
            <p className="text-cyan-100">Grade {currentUser.grade} | View courses, submit assignments, and track your progress</p>
          </div>
        </div>

        <div className="max-w-7xl mx-auto p-6">
          <div className="bg-white rounded-xl shadow-md mb-6">
            <div className="flex border-b">
              <button
                onClick={() => setActiveTab('courses')}
                className={`flex-1 py-4 px-6 font-medium ${activeTab === 'courses' ? 'border-b-2 border-cyan-600 text-cyan-600' : 'text-gray-600'}`}
              >
                📚 My Courses
              </button>
              <button
                onClick={() => setActiveTab('progress')}
                className={`flex-1 py-4 px-6 font-medium ${activeTab === 'progress' ? 'border-b-2 border-cyan-600 text-cyan-600' : 'text-gray-600'}`}
              >
                📈 Progress
              </button>
              <button
                onClick={() => setActiveTab('ai')}
                className={`flex-1 py-4 px-6 font-medium ${activeTab === 'ai' ? 'border-b-2 border-cyan-600 text-cyan-600' : 'text-gray-600'}`}
              >
                🤖 AI Recommendations
              </button>
            </div>

            <div className="p-6">
              {activeTab === 'courses' && (
                <div className="space-y-6">
                  {Object.values(mockData.courses).map(course => (
                    <div key={course.id} className="border-2 border-cyan-200 rounded-lg p-6 bg-cyan-50">
                      <h3 className="text-xl font-bold text-cyan-900 mb-2">{course.name}</h3>
                      <p className="text-gray-700 mb-4">
                        <span className="font-semibold">Teacher:</span> {course.teacher}
                      </p>
                      
                      <div className="space-y-3 ml-4">
                        {Object.values(mockData.assignments).map(assignment => (
                          <div key={assignment.id} className="border-l-4 border-blue-500 pl-4 py-2 bg-blue-50">
                            <p className="font-semibold text-gray-900">{assignment.title}</p>
                            <p className="text-sm text-gray-600 mb-1">{assignment.description}</p>
                            <div className="flex items-center gap-4 text-sm text-gray-700">
                              <span>Due: {assignment.dueDate}</span>
                              <span>Points: {assignment.points}</span>
                              <span className="capitalize">Difficulty: {assignment.difficulty}</span>
                            </div>
                            {assignment.status === 'pending' ? (
                              <div className="mt-2 flex items-center text-orange-600">
                                <Clock className="w-4 h-4 mr-1" />
                                <span className="text-sm font-medium">⏳ Submitted - Pending Grade</span>
                              </div>
                            ) : (
                              <div className="mt-2 flex items-center text-blue-600">
                                <AlertTriangle className="w-4 h-4 mr-1" />
                                <span className="text-sm font-medium">📝 Not submitted (4 days left)</span>
                              </div>
                            )}
                          </div>
                        ))}
                      </div>
                    </div>
                  ))}
                </div>
              )}

              {activeTab === 'progress' && (
                <div className="space-y-6">
                  <div className="bg-blue-50 border-2 border-blue-300 rounded-lg p-6">
                    <h3 className="text-xl font-bold text-blue-900 mb-4 flex items-center">
                      <TrendingUp className="w-6 h-6 mr-2" />
                      Overall Performance
                    </h3>
                    <div className="grid grid-cols-3 gap-4 mb-6">
                      <div className="bg-white p-4 rounded-lg text-center">
                        <div className="text-3xl font-bold text-blue-600">{avgScore.toFixed(1)}%</div>
                        <div className="text-sm text-gray-600 mt-1">Average Grade</div>
                      </div>
                      <div className="bg-white p-4 rounded-lg text-center">
                        <div className="text-3xl font-bold text-green-600">{Math.max(...performance.scores)}%</div>
                        <div className="text-sm text-gray-600 mt-1">Best Score</div>
                      </div>
                      <div className="bg-white p-4 rounded-lg text-center">
                        <div className="text-3xl font-bold text-purple-600">{performance.scores[performance.scores.length - 1]}%</div>
                        <div className="text-sm text-gray-600 mt-1">Recent Score</div>
                      </div>
                    </div>

                    <div className="bg-white p-4 rounded-lg">
                      <h4 className="font-semibold text-gray-900 mb-3">Your Grade Progression</h4>
                      <div className="flex items-end gap-2 h-40">
                        {performance.scores.map((score, idx) => (
                          <div key={idx} className="flex-1 flex flex-col items-center">
                            <div className="text-xs font-medium text-gray-700 mb-1">{score}%</div>
                            <div 
                              className="w-full bg-blue-500 rounded-t transition-all hover:bg-blue-600"
                              style={{ height: `${score}%` }}
                            />
                            <div className="text-xs text-gray-500 mt-1">A{idx + 1}</div>
                          </div>
                        ))}
                      </div>
                    </div>
                  </div>

                  <div className="bg-green-50 border-2 border-green-300 rounded-lg p-6">
                    <div className="flex items-center mb-2">
                      <Award className="w-6 h-6 text-green-600 mr-2" />
                      <h4 className="text-lg font-bold text-green-900">Performance Trend: {performance.trend}</h4>
                    </div>
                    <p className="text-gray-700">Great job! Your grades are improving over time. Keep up the excellent work!</p>
                  </div>
                </div>
              )}

              {activeTab === 'ai' && (
                <div className="space-y-6">
                  <div className="bg-purple-50 border-2 border-purple-300 rounded-lg p-6">
                    <h3 className="text-xl font-bold text-purple-900 mb-4 flex items-center">
                      <Brain className="w-6 h-6 mr-2" />
                      Your Personalized Learning Path
                    </h3>
                    <p className="text-gray-700 mb-4">Based on your performance, we recommend the following resources:</p>
                    
                    <div className="space-y-3">
                      <div className="border-l-4 border-red-500 bg-white p-4 rounded">
                        <div className="flex justify-between items-start mb-1">
                          <span className="font-semibold text-gray-900">Practice: Writing Skills Lab</span>
                          <span className="text-xs font-semibold text-red-600 bg-red-100 px-2 py-1 rounded">High Priority</span>
                        </div>
                        <p className="text-sm text-gray-600">Improve essay structure and grammar</p>
                      </div>

                      <div className="border-l-4 border-green-500 bg-white p-4 rounded">
                        <div className="flex justify-between items-start mb-1">
                          <span className="font-semibold text-gray-900">Enrichment: Advanced Math Challenge</span>
                          <span className="text-xs font-semibold text-orange-600 bg-orange-100 px-2 py-1 rounded">Medium Priority</span>
                        </div>
                        <p className="text-sm text-gray-600">Algebra preview and problem-solving</p>
                      </div>

                      <div className="border-l-4 border-blue-500 bg-white p-4 rounded">
                        <div className="flex justify-between items-start mb-1">
                          <span className="font-semibold text-gray-900">Social: Study Group</span>
                          <span className="text-xs font-semibold text-blue-600 bg-blue-100 px-2 py-1 rounded">Low Priority</span>
                        </div>
                        <p className="text-sm text-gray-600">Collaborate with peers on challenging topics</p>
                      </div>
                    </div>
                  </div>

                  <div className="bg-green-50 border-2 border-green-300 rounded-lg p-6">
                    <h4 className="font-bold text-green-900 mb-3 flex items-center">
                      <BookOpen className="w-5 h-5 mr-2" />
                      Recommended Study Materials
                    </h4>
                    
                    <div className="space-y-3">
                      <div className="bg-white p-3 rounded">
                        <div className="font-semibold text-green-700 mb-1">Grade 7 Mathematics:</div>
                        <ul className="text-sm text-gray-700 space-y-1 ml-4">
                          <li>• Algebraic Expressions</li>
                          <li>• Geometry Foundations</li>
                          <li>• Data Analysis</li>
                        </ul>
                      </div>
                      
                      <div className="bg-white p-3 rounded">
                        <div className="font-semibold text-green-700 mb-1">Grade 7 Science:</div>
                        <ul className="text-sm text-gray-700 space-y-1 ml-4">
                          <li>• Ecosystems Study</li>
                          <li>• Physics Principles</li>
                          <li>• Cell Biology</li>
                        </ul>
                      </div>
                    </div>
                  </div>

                  <div className="bg-blue-50 border-2 border-blue-300 rounded-lg p-6">
                    <h4 className="font-bold text-blue-900 mb-2 flex items-center">
                      <TrendingUp className="w-5 h-5 mr-2" />
                      AI Performance Prediction
                    </h4>
                    <p className="text-gray-700">
                      Based on your current performance trend, we predict you'll score approximately <span className="font-bold text-blue-600">92%</span> on your next math assignment.
                    </p>
                    <p className="text-sm text-gray-600 mt-2">Performance trend: improving ✨</p>
                  </div>
                </div>
              )}
            </div>
          </div>

          <button
            onClick={() => { setCurrentUser(null); setCurrentView('login'); }}
            className="bg-red-500 hover:bg-red-600 text-white py-2 px-6 rounded-lg font-medium transition-colors"
          >
            Logout
          </button>
        </div>
      </div>
    );
  };

  return (
    <div>
      {currentView === 'login' && <LoginScreen />}
      {currentView === 'teacher' && <TeacherDashboard />}
      {currentView === 'student' && <StudentDashboard />}
    </div>
  );
};

export default LMSDemo;