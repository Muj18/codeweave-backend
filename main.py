"use client";

import { useState, useEffect } from "react";
import { saveAs } from "file-saver";
import SyntaxHighlighter from "react-syntax-highlighter/dist/cjs/prism";
import oneDark from "react-syntax-highlighter/dist/cjs/styles/prism/one-dark";
import duotoneLight from "react-syntax-highlighter/dist/cjs/styles/prism/duotone-light";
import { useAuth, useUser } from "@clerk/nextjs";
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";

import {
  FaAws,
  FaMicrosoft,
  FaGoogle,
  FaDocker,
  FaTerminal,
  FaPython,
  FaBug,
  FaRobot,
  FaDatabase,
  FaTools,
  FaCogs,
  FaRocket,
  FaChartBar,
} from "react-icons/fa";
import {
  SiTerraform,
  SiKubernetes,
  SiAnsible,
  SiHelm,
  SiPacker,
  SiHashicorp,
  SiFlux,
  SiJenkins,
  SiGo,
  SiAwslambda,
  SiOpenai,
  SiHuggingface,
  SiPython,
} from "react-icons/si";
import { MdDocumentScanner, MdDataObject } from "react-icons/md";

import Header from "../components/Header";
import Footer from "../components/Footer";
import useLimitCheck from "../components/LimitChecker";
import ClientWrapper from "../components/ClientWrapper";
import UpgradeModal from "../components/UpgradeModal";
import PremiumModal from "../components/PremiumModal";
import JSZip from "jszip";
import toast from "react-hot-toast";

type CodeOutput = string | Record<string, string>;

type CodeBlock = {
  language: string;
  code: string;
};

export default function Page() {
  const { limitReached, incrementUsage, triesLeft, limitError } = useLimitCheck();
  const { getToken } = useAuth();
  const { user } = useUser();

  const [tool, setTool] = useState("Terraform");
  const [prompt, setPrompt] = useState("");
  const [code, setCode] = useState<CodeOutput>("");
  const [cleanedCode, setCleanedCode] = useState<CodeOutput>("");
  const [loading, setLoading] = useState(false);
  const [showSuggestions, setShowSuggestions] = useState(false);
  const [error, setError] = useState("");
  const [showUpgradeModal, setShowUpgradeModal] = useState(false);
  const [showPremiumModal, setShowPremiumModal] = useState(false);
  const [toolChanged, setToolChanged] = useState(false);

  const plan = (user?.unsafeMetadata?.plan as string) || "free";
  const proTools = [
    "Model Fine-Tuning Starter",
    "Model Training Pipeline",
    "LLM Evaluation Toolkit",
    "LLM Deployment",
    "Vector DB",
    "Vault",
    "Jenkins",
    "AWS Lambda",
    "Bash Script",
    "Packer",
    "Azure",
    "GCP",
  ];
  const isPremiumToolLocked = (toolName: string) =>
    proTools.includes(toolName) && !["pro", "teams"].includes(plan);

  const tools = [
    // --- DevOps ---
    {
      name: "AWS",
      icon: <FaAws />,
      description:
        "Provision an S3 bucket, Lambda function, and DynamoDB table with Terraform.",
      suggestions: [
        "Provision an S3 bucket, Lambda function, and DynamoDB table with Terraform.",
      ],
    },
    {
      name: "Azure",
      icon: <FaMicrosoft />,
      description: "Deploy an Azure Kubernetes Service (AKS) cluster with autoscaling enabled.",
      suggestions: ["Deploy an Azure Kubernetes Service (AKS) cluster with autoscaling enabled."],
    },
    {
      name: "GCP",
      icon: <FaGoogle />,
      description: "Set up a GKE cluster and deploy a Node.js API behind a Cloud Load Balancer.",
      suggestions: ["Set up a GKE cluster and deploy a Node.js API behind a Cloud Load Balancer."],
    },
    {
      name: "Terraform",
      icon: <SiTerraform />,
      description: "Generate Terraform code to provision an EC2 instance with security groups.",
      suggestions: ["Generate Terraform code to provision an EC2 instance with security groups."],
    },
    {
      name: "Kubernetes",
      icon: <SiKubernetes />,
      description: "Deploy a Flask app with autoscaling and ConfigMaps in Kubernetes.",
      suggestions: ["Deploy a Flask app with autoscaling and ConfigMaps in Kubernetes."],
    },
    {
      name: "Docker",
      icon: <FaDocker />,
      description: "Create a Dockerfile for a FastAPI app with multi-stage builds and caching.",
      suggestions: ["Create a Dockerfile for a FastAPI app with multi-stage builds and caching."],
    },
    {
      name: "Helm",
      icon: <SiHelm />,
      description: "Create a Helm chart for deploying a multi-service app with ingress rules.",
      suggestions: ["Create a Helm chart for deploying a multi-service app with ingress rules."],
    },
    {
      name: "Flux",
      icon: <SiFlux />,
      description: "Set up a GitOps pipeline using Flux to sync Kubernetes manifests from GitHub.",
      suggestions: ["Set up a GitOps pipeline using Flux to sync Kubernetes manifests from GitHub."],
    },
    {
      name: "Ansible",
      icon: <SiAnsible />,
      description: "Write an Ansible playbook to install Docker and configure a firewall on Ubuntu.",
      suggestions: ["Write an Ansible playbook to install Docker and configure a firewall on Ubuntu."],
    },
    {
      name: "Vault",
      icon: <SiHashicorp />,
      description: "Use HashiCorp Vault to store and retrieve secrets for a production app.",
      suggestions: ["Use HashiCorp Vault to store and retrieve secrets for a production app."],
    },
    {
      name: "Jenkins",
      icon: <SiJenkins />,
      description: "Build a Jenkins pipeline to test, build, and deploy a Java microservice.",
      suggestions: ["Build a Jenkins pipeline to test, build, and deploy a Java microservice."],
    },
    {
      name: "Packer",
      icon: <SiPacker />,
      description: "Create a Packer template to build a custom AMI with NGINX and fail2ban.",
      suggestions: ["Create a Packer template to build a custom AMI with NGINX and fail2ban."],
    },
    {
      name: "Bash Script",
      icon: <FaTerminal />,
      description: "Write a bash script to back up logs and clean up temp files daily.",
      suggestions: ["Write a bash script to back up logs and clean up temp files daily."],
    },
    {
      name: "Python Script",
      icon: <FaPython />,
      description: "Build a Python script that renames files based on a CSV mapping.",
      suggestions: ["Build a Python script that renames files based on a CSV mapping."],
    },
    {
      name: "Go Script",
      icon: <SiGo />,
      description: "Create a Go CLI tool that monitors disk usage and sends alerts.",
      suggestions: ["Create a Go CLI tool that monitors disk usage and sends alerts."],
    },
    {
      name: "AWS Lambda",
      icon: <SiAwslambda />,
      description: "Create a Lambda function to resize uploaded S3 images using Python.",
      suggestions: ["Create a Lambda function to resize uploaded S3 images using Python."],
    },

    // --- GenAI ---
    {
      name: "Chatbot Builder",
      icon: <FaRobot />,
      description: "Create a chatbot that answers customer FAQs using a custom knowledge base.",
      suggestions: ["Create a chatbot that answers customer FAQs using a custom knowledge base."],
    },
    {
      name: "PDF / Document QA Bot",
      icon: <MdDocumentScanner />,
      description: "Build a QA bot that extracts answers from uploaded PDF invoices.",
      suggestions: ["Build a QA bot that extracts answers from uploaded PDF invoices."],
    },
    {
      name: "RAG Pipeline",
      icon: <FaDatabase />,
      description:
        "Create a RAG pipeline that uses Pinecone for vector storage and OpenAI for generation.",
      suggestions: ["Create a RAG pipeline that uses Pinecone for vector storage and OpenAI for generation."],
    },
    {
      name: "Data Preprocessing Pipeline",
      icon: <MdDataObject />,
      description: "Clean, normalize, and split a dataset of product reviews for fine-tuning.",
      suggestions: ["Clean, normalize, and split a dataset of product reviews for fine-tuning."],
    },
    {
      name: "FastAPI Backend for GenAI",
      icon: <FaCogs />,
      description: "Expose a GPT-4 based sentiment analyzer using FastAPI.",
      suggestions: ["Expose a GPT-4 based sentiment analyzer using FastAPI."],
    },
    {
      name: "Agent & Tool Builder",
      icon: <FaTools />,
      description: "Build an agent that scrapes job listings and updates a Notion table.",
      suggestions: ["Build an agent that scrapes job listings and updates a Notion table."],
    },
    {
      name: "Model Fine-Tuning Starter",
      icon: <SiOpenai />,
      description: "Fine-tune a LLaMA model on a custom dataset of financial documents.",
      suggestions: ["Fine-tune a LLaMA model on a custom dataset of financial documents."],
    },
    {
      name: "Model Training Pipeline",
      icon: <SiHuggingface />,
      description:
        "Build a training pipeline for a classification model using PyTorch and Hugging Face.",
      suggestions: ["Build a training pipeline for a classification model using PyTorch and Hugging Face."],
    },
    {
      name: "LLM Evaluation Toolkit",
      icon: <FaChartBar />,
      description:
        "Evaluate three LLMs using accuracy and latency benchmarks on a summarization task.",
      suggestions: ["Evaluate three LLMs using accuracy and latency benchmarks on a summarization task."],
    },
    {
      name: "LLM Deployment",
      icon: <FaRocket />,
      description:
        "Deploy a Falcon-7B model using Hugging Face Transformers and a GPU Docker container.",
      suggestions: ["Deploy a Falcon-7B model using Hugging Face Transformers and a GPU Docker container."],
    },
    {
      name: "Vector DB",
      icon: <FaDatabase />,
      description:
        "Set up a vector DB pipeline using FAISS to search support articles with embeddings.",
      suggestions: ["Set up a vector DB pipeline using FAISS to search support articles with embeddings."],
    },
    {
      name: "Streamlit Dashboard",
      icon: <SiPython />,
      description: "Build a Streamlit dashboard to visualize model performance metrics from a CSV.",
      suggestions: ["Build a Streamlit dashboard to visualize model performance metrics from a CSV."],
    },
    {
      name: "Streamlit App",
      icon: <SiPython />,
      description: "Create fast data apps or prototypes with a web interface.",
      suggestions: ["Create fast data apps or prototypes with a web interface."],
    },
    {
      name: "LangChain",
      icon: <FaRobot />,
      description: "Build a LangChain agent that queries a local PDF file and answers questions.",
      suggestions: ["Build a LangChain agent that queries a local PDF file and answers questions."],
    },
    {
      name: "Fine-tuning",
      icon: <SiOpenai />,
      description: "Improve models by training on custom labeled data.",
      suggestions: ["Improve models by training on custom labeled data."],
    },
    {
      name: "OpenAI API",
      icon: <SiOpenai />,
      description: "Use OpenAI API to summarize meeting transcripts into action items.",
      suggestions: ["Use OpenAI API to summarize meeting transcripts into action items."],
    },
    {
      name: "Hugging Face",
      icon: <SiHuggingface />,
      description: "Use pre-trained AI models or deploy your own on the HF Hub.",
      suggestions: ["Use pre-trained AI models or deploy your own on the HF Hub."],
    },
    {
      name: "Agent & Tools",
      icon: <FaTools />,
      description: "Combine agents with external tools to complete complex tasks.",
      suggestions: ["Combine agents with external tools to complete complex tasks."],
    },
    {
      name: "FastAPI Backend",
      icon: <FaCogs />,
      description: "Create API backends for serving logic, data, or models.",
      suggestions: ["Create API backends for serving logic, data, or models."],
    },

    // --- Troubleshooting ---
    {
      name: "Troubleshooting",
      icon: <FaBug />,
      description: "Identify, debug, and fix issues across your stack or codebase.",
      suggestions: ["Identify, debug, and fix issues across your stack or codebase."],
    },

    // --- Other ---
    {
      name: "Other",
      icon: <FaCogs />,
      description: "Build a tool that converts Markdown notes into a searchable SQLite DB.",
      suggestions: ["Build a tool that converts Markdown notes into a searchable SQLite DB."],
    },
  ];

  const selected = tools.find((t) => t.name === tool);
  const suggestions =
    selected?.suggestions?.filter((s) =>
      s.toLowerCase().includes(prompt.toLowerCase())
    ) || [];

  const extractCodeBlocks = (text: string): CodeBlock[] => {
    const regex = /```(\w+)?\n([\s\S]*?)```/g;
    const blocks: CodeBlock[] = [];
    let match;
    while ((match = regex.exec(text))) {
      blocks.push({
        language: (match[1] || "").toLowerCase(),
        code: match[2].trim(),
      });
    }
    return blocks;
  };

  const getLanguage = (tool: string): string => {
    if (tool.includes("Terraform")) return "hcl";
    if (tool.includes("Python")) return "python";
    if (tool.includes("Bash")) return "bash";
    if (tool.includes("Docker")) return "dockerfile";
    if (tool.includes("Kubernetes") || tool.includes("Helm")) return "yaml";
    if (tool.includes("Go")) return "go";
    if (tool.includes("Jenkins")) return "groovy";
    if (tool.includes("Packer")) return "hcl";
    if (tool.includes("Vault")) return "hcl";
    if (tool.includes("Fine-tuning") || tool.includes("LLM Evaluation")) return "json";
    if (tool.includes("FastAPI") || tool.includes("LLM") || tool.includes("LangChain")) return "python";
    return "text";
  };

  const getFileExtension = (input: string): string => {
    const val = (input || "").toLowerCase();
    if (["python", "py", "python script"].includes(val)) return "py";
    if (["bash", "shell", "sh", "bash script"].includes(val)) return "sh";
    if (["yaml", "yml", "helm", "flux"].includes(val)) return "yaml";
    if (["json"].includes(val)) return "json";
    if (["go", "golang", "go script"].includes(val)) return "go";
    if (["dockerfile", "docker"].includes(val)) return "Dockerfile";
    if (["hcl", "terraform"].includes(val)) return "tf";
    if (["jenkins", "jenkinsfile"].includes(val)) return "jenkinsfile";
    if (["packer", "pkr.hcl"].includes(val)) return "pkr.hcl";
    if (["text", "txt"].includes(val)) return "txt";
    if (
      [
        "fastapi",
        "openai api",
        "hugging face",
        "streamlit",
        "streamlit app",
        "langchain",
        "rag pipeline",
        "llm evaluation toolkit",
        "llm deployment",
        "agent & tool builder",
        "agent & tools",
        "fastapi backend",
        "fastapi backend for genai",
        "model fine-tuning starter",
        "model training pipeline",
        "fine-tuning",
      ].includes(val)
    )
      return "py";
    if (["ansible"].includes(val)) return "yml";
    if (["aws lambda"].includes(val)) return "py";
    if (["pdf / document qa bot", "chatbot builder", "vector db", "data preprocessing pipeline"].includes(val))
      return "py";
    if (["markdown", "md"].includes(val)) return "md";
    if (["html", "web", "react"].includes(val)) return "html";

    if (val.includes("terraform")) return "tf";
    if (val.includes("docker")) return "Dockerfile";
    if (val.includes("vault")) return "hcl";
    if (val.includes("jenkins")) return "jenkinsfile";
    if (val.includes("packer")) return "pkr.hcl";
    if (val.includes("helm")) return "yaml";
    if (val.includes("flux")) return "yaml";
    if (val.includes("ansible")) return "yml";
    if (val.includes("bash")) return "sh";
    if (val.includes("python")) return "py";
    if (val.includes("go")) return "go";
    if (val.includes("yaml") || val.includes("yml")) return "yaml";
    if (val.includes("json")) return "json";
    return "txt";
  };

  function parseNamedCodeBlocks(text: string): Record<string, string> {
    const files: Record<string, string> = {};

    // **filename.ext**
    const markdownRegex =
      /(?:\*\*)?([a-zA-Z0-9_.\-]+\.\w+)(?:\*\*)?\s*:?\s*[\r\n]*```[\w+-]*[\r\n]+([\s\S]*?)```/g;
    let match;
    while ((match = markdownRegex.exec(text)) !== null) {
      const filename = match[1].trim();
      const content = match[2].trim();
      files[filename] = content;
    }

    // "# Script to X" -> script_to_x.sh
    const headingCodeRegex =
      /#\s*(Script to .+?)\s*[\r\n]+```(?:bash|sh)?[\r\n]+([\s\S]*?)```/g;
    while ((match = headingCodeRegex.exec(text)) !== null) {
      const rawTitle = match[1].trim();
      const content = match[2].trim();
      const filenameBase = rawTitle
        .replace(/^Script to /i, "")
        .replace(/[^a-zA-Z0-9 ]/g, "")
        .trim()
        .toLowerCase()
        .replace(/\s+/g, "_");
      const filename = `${filenameBase}.sh`;
      files[filename] = content;
    }

    // "1. Title:" lines
    const numberedRegex =
      /^\s*\d+\.\s+(.+?):\s*[\r\n]+```(?:bash|sh)?[\r\n]+([\s\S]*?)```/gm;
    while ((match = numberedRegex.exec(text)) !== null) {
      const rawTitle = match[1].trim();
      const content = match[2].trim();
      const filenameBase = rawTitle
        .replace(/[^a-zA-Z0-9 ]/g, "")
        .trim()
        .toLowerCase()
        .replace(/\s+/g, "_");
      const filename = `${filenameBase}.sh`;
      files[filename] = content;
    }

    return files;
  }

  function cleanDisplayOutput(text: string): string {
    // For audits/reports we KEEP markdown; for pure code we strip fences when downloading
    return text.replace(/\n*\.\.\.\s*$/g, "").trim();
  }

  const handleGenerate = async () => {
    if (!prompt && !limitReached) return;

    if (limitReached) {
      setShowUpgradeModal(true);
      return;
    }

    setLoading(true);
    setCode("");
    setError("");

    try {
      const token = await getToken();
      const res = await fetch("/api/generate", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: token ? `Bearer ${token}` : "",
        },
        body: JSON.stringify({ tool, prompt }),
      });

      const ct = res.headers.get("content-type") || "";
      if (!res.ok) {
        const errText = ct.includes("application/json")
          ? JSON.stringify(await res.json())
          : await res.text();
        setError(`Server error ${res.status}: ${errText}`);
        setLoading(false);
        return;
      }

      // Accept either text/plain or JSON
      let generated = "";
      if (ct.includes("text/plain")) {
        generated = await res.text();
      } else {
        const json = await res.json();
        generated =
          typeof json === "string"
            ? json
            : json.result || json.output || JSON.stringify(json, null, 2);
      }

      const display = cleanDisplayOutput(generated);
      setCleanedCode(display);
      setCode(display || "No output returned.");

      if (plan === "free") {
        await incrementUsage();
        if (limitError) setError(limitError);
      }
    } catch (err: any) {
      setError("Error connecting to backend.");
      console.error("Generate request failed:", err);
    } finally {
      setLoading(false);
      setShowSuggestions(false);
    }
  };

  const syntaxStyle =
    typeof window !== "undefined" &&
    window.matchMedia("(prefers-color-scheme: dark)").matches
      ? oneDark
      : duotoneLight;

  const shouldRenderAsCode = (toolName: string, content: string): boolean => {
    const lang = getLanguage(toolName);
    if (lang !== "text") return true;
    const codeFenceCount = (content.match(/```/g) || []).length;
    return codeFenceCount >= 4;
  };

  // Simple download handler for multi-file or single-file outputs
  const handleDownload = async () => {
    if (!cleanedCode || typeof cleanedCode !== "string") return;

    const files = parseNamedCodeBlocks(cleanedCode);
    const hasNamedFiles = Object.keys(files).length > 0;

    if (hasNamedFiles) {
      const zip = new JSZip();
      for (const [filename, content] of Object.entries(files)) {
        zip.file(filename, content);
      }
      const blob = await zip.generateAsync({ type: "blob" });
      saveAs(blob, "codeweave_output.zip");
      toast.success("Downloaded codeweave_output.zip");
      return;
    }

    const lang = getLanguage(tool);
    const ext = getFileExtension(tool || lang);
    const blocks = extractCodeBlocks(cleanedCode);
    const body =
      blocks.length > 0 ? blocks.map((b) => b.code).join("\n\n") : cleanedCode;
    const blob = new Blob([body], { type: "text/plain;charset=utf-8" });
    saveAs(blob, `output.${ext}`);
    toast.success(`Downloaded output.${ext}`);
  };

  const asString = typeof cleanedCode === "string" ? cleanedCode : "";

  return (
    <ClientWrapper>
      <div className="bg-white dark:bg-gray-900 text-gray-900 dark:text-white min-h-screen flex flex-col">
        <Header />
        <main className="flex-1 max-w-full mx-8 p-0 sm:p-6 lg:p-8 space-y-6">
          <h1 className="text-4xl font-bold text-center pt-2 text-blue-600">
            Select Your DevOps & AI Focus Areas
          </h1>
          <p className="text-lg text-center pb-4 text-gray-700 dark:text-gray-300">
            Select your DevOps and AI focus areas to generate code, streamline workflows, and accelerate delivery with AI-powered automation
          </p>

          <div className="flex justify-center mb-6">
            <button
              onClick={() =>
                document.getElementById("copilot")?.scrollIntoView({ behavior: "smooth" })
              }
              style={{
                fontSize: "12px",
                fontFamily: "sans-serif",
                backgroundColor: "#1D4ED8",
                borderRadius: "6px",
                color: "#fff",
                display: "flex",
                alignItems: "center",
                gap: "10px",
                padding: "9px 13px",
                cursor: "pointer",
                border: "1px solid rgba(255, 255, 255, 0.3)",
              }}
            >
              Launch Copilot
              <svg
                xmlns="http://www.w3.org/2000/svg"
                width="16"
                height="16"
                viewBox="0 0 24 24"
                fill="none"
                stroke="white"
                strokeWidth="2"
                strokeLinecap="round"
                strokeLinejoin="round"
              >
                <line x1="7" y1="17" x2="17" y2="7" />
                <polyline points="7 7 17 7 17 17" />
              </svg>
            </button>
          </div>

          <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-4">
            {tools.map((t) => (
              <button
                key={t.name}
                onClick={() => {
                  if (isPremiumToolLocked(t.name)) {
                    setShowPremiumModal(true);
                  } else {
                    setToolChanged(true);
                    setTool(t.name);
                    setPrompt("");
                  }
                }}
                className={`relative flex items-center justify-between max-w-sm gap-2 p-4 rounded-lg shadow-md border text-sm transition m-auto sm:m-0 w-full ms:w-auto ${
                  t.name === tool
                    ? "bg-indigo-600 text-white dark:bg-indigo-500"
                    : "bg-gray-100 dark:bg-gray-700 dark:text-white hover:border-indigo-300 hover:scale-105"
                } dark:bg-gray-800`}
              >
                <div className="flex items-center justify-center">
                  <div className="bg-blue-100 text-blue-700 p-2 rounded-lg">
                    {t.icon}
                  </div>
                  <div className="ml-3 text-left">
                    <h3
                      className={`flex justify-between items-start text-base font-semibold gap-2 ${
                        t.name === tool ? "text-white" : "text-gray-900 dark:text-white"
                      }`}
                    >
                      {t.name}
                    </h3>
                    <p
                      className={`text-sm ${
                        t.name === tool ? "text-white" : "text-gray-500 dark:text-gray-400"
                      }`}
                    />
                  </div>
                </div>
                {proTools.includes(t.name) && !["pro", "teams"].includes(plan) && (
                  <span
                    className="ml-1 translate-y-[-2px] text-yellow-500 cursor-help"
                    title="Pro Feature – Upgrade to unlock"
                  >
                    👑
                  </span>
                )}
              </button>
            ))}
          </div>

          <div className="w-full sm:w-[70%] flex flex-col mx-auto" id="copilot">
            <div className="flex flex-col items-center py-4">
              <h1 className="text-4xl font-bold text-center py-3 text-blue-600">
                Chat with Your DevOps & AI Copilot
              </h1>
              <p className="text-lg text-center pb-4 text-gray-700 dark:text-gray-300">
                Describe your challenge and get AI-powered help with DevOps, GenAI, or infrastructure troubleshooting
              </p>

              <div className="relative w-full mx-auto">
                <textarea
                  value={prompt}
                  maxLength={8000}
                  onFocus={() => setShowSuggestions(true)}
                  onBlur={() => setTimeout(() => setShowSuggestions(false), 100)}
                  onChange={(e) => {
                    setPrompt(e.target.value);
                    setShowSuggestions(true);
                  }}
                  placeholder={
                    toolChanged
                      ? tools.find((t) => t.name === tool)?.description ?? ""
                      : "Describe your setup or issue to fix..."
                  }
                  className="w-full max-h[400px] min-h-[180px] p-3 border rounded dark:bg-gray-700 dark:text-white overflow-auto resize-y"
                />

                <div className="text-right text-xs text-gray-500 dark:text-gray-400 mt-1">
                  {prompt.length.toLocaleString()} / 8,000
                </div>

                {showSuggestions && suggestions.length > 0 && (
                  <ul className="absolute translate-y-[-20px] left-0 right-0 max-h-56 overflow-y-auto bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-600 rounded-xl shadow-lg z-20 divide-y divide-gray-100 dark:divide-gray-700">
                    {suggestions.map((s, i) => (
                      <li
                        key={i}
                        onMouseDown={() => {
                          setPrompt(s);
                          setShowSuggestions(false);
                        }}
                        className="px-5 py-3 text-sm text-gray-800 dark:text-white hover:bg-indigo-50 dark:hover:bg-gray-700 cursor-pointer transition"
                      >
                        {s}
                      </li>
                    ))}
                    <li className="px-5 py-3 text-sm text-gray-800 dark:text-white hover:bg-indigo-50 dark:hover:bg-gray-700 cursor-pointer transition">
                      Got your own idea? Type it here!
                    </li>
                  </ul>
                )}
              </div>
            </div>

            <div className="flex items-center gap-3">
              <button
                onClick={handleGenerate}
                disabled={loading}
                className={`flex justify-center items-center gap-2 bg-blue-700 hover:bg-blue-900 text-white font-bold py-2 px-6 rounded transition
                  ${limitReached ? "w-[190px]" : "w-[150px]"}
                  ${loading || limitReached ? "opacity-50" : ""}`}
              >
                {loading ? "Generating..." : limitReached ? "Upgrade to Continue" : "Generate"}
              </button>
              {asString && (
                <button
                  onClick={handleDownload}
                  className="border border-gray-300 dark:border-gray-600 px-4 py-2 rounded hover:bg-gray-100 dark:hover:bg-gray-700"
                >
                  Download Output
                </button>
              )}
            </div>

            {error && (
              <div className="mt-4 p-3 rounded border border-red-300 bg-red-50 text-red-800 dark:bg-red-900/30 dark:text-red-200">
                {error}
              </div>
            )}

            {/* OUTPUT */}
            {asString && (
              <div className="mt-6 p-4 border rounded bg-gray-50 dark:bg-gray-900 dark:text-gray-200">
                {shouldRenderAsCode(tool, asString) ? (
                  <SyntaxHighlighter
                    language={getLanguage(tool)}
                    style={syntaxStyle as any}
                    customStyle={{ margin: 0, background: "transparent" }}
                    wrapLongLines
                  >
                    {asString}
                  </SyntaxHighlighter>
                ) : (
                  <ReactMarkdown className="prose prose-sm sm:prose lg:prose-lg dark:prose-invert max-w-none" remarkPlugins={[remarkGfm]}>
                    {asString}
                  </ReactMarkdown>
                )}
              </div>
            )}
          </div>
        </main>

        <Footer />
      </div>

      {/* Modals */}
      {showUpgradeModal && (
        <UpgradeModal
          isOpen={showUpgradeModal}
          onClose={() => setShowUpgradeModal(false)}
          triesLeft={triesLeft}
        />
      )}
      {showPremiumModal && (
        <PremiumModal
          isOpen={showPremiumModal}
          onClose={() => setShowPremiumModal(false)}
        />
      )}
    </ClientWrapper>
  );
}
